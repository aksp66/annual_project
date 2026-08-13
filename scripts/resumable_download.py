#!/usr/bin/env python
"""Download files with HTTP Range resume + retries, for unstable connections.

Downloads Fashion-MNIST (and can be reused for CIFAR-10) raw files directly,
resuming from the last received byte on connection drop instead of restarting
from scratch. Left in scripts/ as a reusable fallback when torchvision's
built-in downloader keeps failing on a flaky network.
"""
import time
from pathlib import Path

import requests

FASHION_MNIST_BASE = "http://fashion-mnist.s3-website.eu-central-1.amazonaws.com/"
FASHION_MNIST_FILES = [
    "train-images-idx3-ubyte.gz",
    "train-labels-idx1-ubyte.gz",
    "t10k-images-idx3-ubyte.gz",
    "t10k-labels-idx1-ubyte.gz",
]

CIFAR10_URL = "https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz"

TARGET_DIR = Path("data") / "raw" / "FashionMNIST" / "raw"
CIFAR10_TARGET_DIR = Path("data") / "raw"
CHUNK_SIZE = 32 * 1024
MAX_RETRIES = 50
TIMEOUT = 30


def download_with_resume(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(1, MAX_RETRIES + 1):
        existing = dest.stat().st_size if dest.exists() else 0
        headers = {"Range": f"bytes={existing}-"} if existing else {}
        try:
            with requests.get(url, headers=headers, stream=True, timeout=TIMEOUT) as r:
                if r.status_code == 416:
                    print(f"{dest.name}: already complete")
                    return
                r.raise_for_status()
                total = r.headers.get("Content-Length")
                mode = "ab" if existing else "wb"
                with open(dest, mode) as f:
                    for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
                        if chunk:
                            f.write(chunk)
                size = dest.stat().st_size
                print(f"{dest.name}: {size} bytes downloaded")
                if total is not None and r.status_code == 200 and size >= int(total):
                    return
                if r.status_code == 206:
                    return
        except (requests.exceptions.RequestException, ConnectionError) as e:
            wait = min(5 * attempt, 30)
            got = dest.stat().st_size if dest.exists() else 0
            print(f"{dest.name}: attempt {attempt} failed ({e}); have {got} bytes; retry in {wait}s")
            time.sleep(wait)
            continue
    raise RuntimeError(f"Failed to download {url} after {MAX_RETRIES} attempts")


def main():
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "fashion_mnist"
    if target == "fashion_mnist":
        for fname in FASHION_MNIST_FILES:
            url = FASHION_MNIST_BASE + fname
            dest = TARGET_DIR / fname
            print(f"=== {fname} ===")
            download_with_resume(url, dest)
    elif target == "cifar10":
        dest = CIFAR10_TARGET_DIR / "cifar-10-python.tar.gz"
        print(f"=== {dest.name} ===")
        download_with_resume(CIFAR10_URL, dest)
    else:
        raise SystemExit(f"Unknown target: {target}")
    print("Done.")


if __name__ == "__main__":
    main()
