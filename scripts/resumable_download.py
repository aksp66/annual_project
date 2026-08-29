#!/usr/bin/env python
"""Download + extract Fashion-MNIST / CIFAR-10 with HTTP Range resume + retries.

Used as a fallback when torchvision's built-in downloader keeps failing on a
flaky network (see HISTORY.md 2026-08-22). Self-sufficient: downloads,
verifies the checksum against the same values torchvision uses, and extracts
— running this alone is enough to make the dataset loadable by torchvision
afterwards (download=False).
"""
import gzip
import hashlib
import shutil
import tarfile
import time
from pathlib import Path

import requests

FASHION_MNIST_BASE = "http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/"
# (filename, md5) — same values as torchvision.datasets.FashionMNIST.resources
FASHION_MNIST_FILES = [
    ("train-images-idx3-ubyte.gz", "8d4fb7e6c68d591d4c3dfef9ec88bf0d"),
    ("train-labels-idx1-ubyte.gz", "25c81989df183df01b3e8a0aad5dffbe"),
    ("t10k-images-idx3-ubyte.gz", "bef4ecab320f06d8554ea6380940ec79"),
    ("t10k-labels-idx1-ubyte.gz", "bb300cfdad3c16e7a12a480ee83cd310"),
]

CIFAR10_URL = "https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz"
CIFAR10_MD5 = "c58f30108f718f92721af3b95e74349a"  # torchvision.datasets.CIFAR10.tgz_md5

FASHION_MNIST_DIR = Path("data") / "raw" / "FashionMNIST" / "raw"
CIFAR10_DIR = Path("data") / "raw"
CHUNK_SIZE = 32 * 1024
MAX_RETRIES = 50
TIMEOUT = 30


def file_md5(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def download_with_resume(url: str, dest: Path, expected_md5: str) -> None:
    """Download url to dest, resuming on drop. Restarts from scratch whenever
    the server doesn't actually honor the Range request (status != 206), so a
    partial file is never silently extended with a full-content response."""
    dest.parent.mkdir(parents=True, exist_ok=True)

    if dest.exists() and file_md5(dest) == expected_md5:
        print(f"{dest.name}: already downloaded and verified")
        return

    for attempt in range(1, MAX_RETRIES + 1):
        existing = dest.stat().st_size if dest.exists() else 0
        headers = {"Range": f"bytes={existing}-"} if existing else {}
        try:
            with requests.get(url, headers=headers, stream=True, timeout=TIMEOUT) as r:
                if r.status_code == 416:
                    # Range not satisfiable: local file is already >= remote size, re-verify from scratch.
                    dest.unlink()
                    continue
                r.raise_for_status()

                resumed = existing > 0 and r.status_code == 206
                mode = "ab" if resumed else "wb"
                if existing > 0 and not resumed:
                    print(f"{dest.name}: server ignored Range (status {r.status_code}); restarting from 0")

                with open(dest, mode) as f:
                    for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
                        if chunk:
                            f.write(chunk)
                print(f"{dest.name}: {dest.stat().st_size} bytes downloaded")
        except (requests.exceptions.RequestException, ConnectionError) as e:
            wait = min(5 * attempt, 30)
            got = dest.stat().st_size if dest.exists() else 0
            print(f"{dest.name}: attempt {attempt} failed ({e}); have {got} bytes; retry in {wait}s")
            time.sleep(wait)
            continue

        if dest.exists() and file_md5(dest) == expected_md5:
            return
        print(f"{dest.name}: checksum mismatch after download, retrying")
        dest.unlink()

    raise RuntimeError(f"Failed to download {url} with a verified checksum after {MAX_RETRIES} attempts")


def extract_gzip(src: Path, dest: Path) -> None:
    with gzip.open(src, "rb") as f_in, open(dest, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)


def fetch_fashion_mnist() -> None:
    for fname, md5 in FASHION_MNIST_FILES:
        url = FASHION_MNIST_BASE + fname
        gz_path = FASHION_MNIST_DIR / fname
        print(f"=== {fname} ===")
        download_with_resume(url, gz_path, md5)
        extracted = FASHION_MNIST_DIR / fname[:-3]  # strip ".gz"
        if not extracted.exists():
            extract_gzip(gz_path, extracted)
            print(f"{fname}: extracted to {extracted}")


def fetch_cifar10() -> None:
    dest = CIFAR10_DIR / "cifar-10-python.tar.gz"
    print(f"=== {dest.name} ===")
    download_with_resume(CIFAR10_URL, dest, CIFAR10_MD5)
    if not (CIFAR10_DIR / "cifar-10-batches-py").exists():
        with tarfile.open(dest) as tar:
            tar.extractall(CIFAR10_DIR, filter="data")
        print(f"{dest.name}: extracted to {CIFAR10_DIR / 'cifar-10-batches-py'}")


def main():
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "fashion_mnist"
    if target == "fashion_mnist":
        fetch_fashion_mnist()
    elif target == "cifar10":
        fetch_cifar10()
    else:
        raise SystemExit(f"Unknown target: {target}")
    print("Done.")


if __name__ == "__main__":
    main()
