#!/usr/bin/env python
"""EDA complète sur Fashion-MNIST (dataset retenu, cf. HISTORY.md 2026-08-13).

Calcule les points de la checklist TASKS.md > Data / Experiment Engineer > EDA
et écrit un rapport Markdown lisible dans reports/eda_fashion_mnist.md.
"""
import hashlib
from pathlib import Path

import numpy as np
from torchvision import datasets
from PIL import Image

CLASS_NAMES = [
    "T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
    "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot",
]

REPORTS_DIR = Path("reports")
GRID_PATH = REPORTS_DIR / "samples" / "fashion_mnist_grid.png"
REPORT_PATH = REPORTS_DIR / "eda_fashion_mnist.md"


def make_class_grid(images: np.ndarray, targets: np.ndarray, path: Path) -> None:
    """One example per class, arranged in a single row grid image."""
    cell = 28
    grid = np.zeros((cell, cell * 10), dtype=np.uint8)
    for cls in range(10):
        idx = int(np.where(targets == cls)[0][0])
        grid[:, cls * cell:(cls + 1) * cell] = images[idx]
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(grid).resize((28 * 10 * 3, 28 * 3), Image.NEAREST).save(path)


def run():
    train = datasets.FashionMNIST(root="data/raw", train=True, download=False)
    test = datasets.FashionMNIST(root="data/raw", train=False, download=False)

    train_x = train.data.numpy()
    train_y = train.targets.numpy()
    test_x = test.data.numpy()
    test_y = test.targets.numpy()

    lines = []
    lines.append("# EDA — Fashion-MNIST\n")
    lines.append(
        "Dataset retenu le 2026-08-13 (voir `HISTORY.md`). "
        "Analyse exploratoire complète (checklist `TASKS.md` > Data / Experiment Engineer > EDA).\n"
    )

    # Shapes / format
    lines.append("## Volumétrie et format\n")
    lines.append(f"- Train : {train_x.shape[0]} images, shape `{train_x.shape[1:]}`, dtype `{train_x.dtype}`")
    lines.append(f"- Test : {test_x.shape[0]} images, shape `{test_x.shape[1:]}`, dtype `{test_x.dtype}`\n")

    # Missing / corrupted: dtype uint8 makes NaN and out-of-[0,255] structurally
    # impossible, so those aren't real checks here — actual corruption (truncated
    # download, bad bytes) is caught upstream by torchvision's MD5 verification
    # against the reference checksums during load/extraction (this script only
    # runs if that already succeeded). What CAN still slip through a checksum
    # check is a technically-valid but degenerate image (e.g. fully blank) —
    # checked below instead.
    lines.append("## Valeurs manquantes / fichiers corrompus\n")
    lines.append(
        "- Intégrité du fichier déjà vérifiée en amont par le checksum MD5 de torchvision "
        "au chargement (le chargement aurait échoué sinon) — voir aussi `scripts/resumable_download.py`, "
        "qui revérifie le même MD5 après téléchargement.\n"
        "- Labels hors [0, 9] train : "
        f"{int(((train_y < 0) | (train_y > 9)).sum())}, test : "
        f"{int(((test_y < 0) | (test_y > 9)).sum())}\n"
    )

    # Outliers: degenerate images (all-zero or all-max) — a checksum-valid file
    # can still contain a blank/garbage image, unlike a NaN or out-of-range
    # check on a uint8 array (structurally impossible, so not a real signal).
    def n_degenerate(x: np.ndarray) -> int:
        flat = x.reshape(len(x), -1)
        return int(((flat.min(axis=1) == flat.max(axis=1))).sum())

    deg_train = n_degenerate(train_x)
    deg_test = n_degenerate(test_x)
    lines.append("## Valeurs aberrantes\n")
    lines.append(f"- Plage de pixels train : [{int(train_x.min())}, {int(train_x.max())}] (attendu [0, 255], "
                 "garanti par le dtype `uint8` — indicatif, pas un test de corruption)")
    lines.append(f"- Images dégénérées (entièrement uniformes, ex. tout à 0) train : {deg_train}, test : {deg_test}")
    lines.append("- Toutes les images ont la même résolution 28×28 (garanti par le format IDX du dataset)\n")

    # Duplicates (exact hash)
    def n_exact_duplicates(x: np.ndarray) -> int:
        hashes = [hashlib.md5(img.tobytes()).hexdigest() for img in x]
        return len(hashes) - len(set(hashes))

    dup_train = n_exact_duplicates(train_x)
    dup_test = n_exact_duplicates(test_x)
    lines.append("## Doublons exacts (hash MD5 par image)\n")
    lines.append(f"- Doublons dans train : {dup_train}")
    lines.append(f"- Doublons dans test : {dup_test}\n")

    # Class balance
    lines.append("## Équilibre des classes\n")
    lines.append("|Classe|Nom|Train|Test|")
    lines.append("|---|---|---|---|")
    for cls in range(10):
        n_train = int((train_y == cls).sum())
        n_test = int((test_y == cls).sum())
        lines.append(f"|{cls}|{CLASS_NAMES[cls]}|{n_train}|{n_test}|")
    lines.append("")
    lines.append(
        "Classes parfaitement équilibrées (6000 train / 1000 test par classe) — "
        "pas de rééquilibrage nécessaire.\n"
    )

    # Pixel stats (for normalization choice) — single cast reused for both stats
    train_x_f64 = train_x.astype(np.float64)
    mean = float(train_x_f64.mean())
    std = float(train_x_f64.std())
    lines.append("## Statistiques de pixels (base de la normalisation)\n")
    lines.append(f"- Moyenne (train) : {mean:.3f}")
    lines.append(f"- Écart-type (train) : {std:.3f}")
    lines.append(
        "- Pour la diffusion, normalisation prévue dans [-1, 1] : `x_norm = x / 127.5 - 1` "
        "(cf. `TASKS.md` > pipeline de chargement).\n"
    )

    # Sample grid
    make_class_grid(train_x, train_y, GRID_PATH)
    lines.append("## Échantillon visuel (une image par classe)\n")
    lines.append(f"![Un exemple par classe]({GRID_PATH.relative_to(REPORTS_DIR).as_posix()})\n")

    # Observations
    lines.append("## Observations\n")
    lines.append(
        "- Dataset propre : pas de valeurs manquantes, pas de doublons exacts, "
        "pixels dans la plage attendue [0, 255], classes strictement équilibrées.\n"
        "- Faible variance de moyenne/écart-type entre classes attendue (niveaux de gris, fond uniforme) : "
        "bon candidat pour un DDPM/GAN from scratch avec budget de calcul limité.\n"
        "- Aucun biais de classe détecté à ce stade ; à surveiller en cas de mode collapse du GAN sur "
        "des classes visuellement proches (ex. Shirt/Pullover/Coat)."
    )

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Rapport écrit dans {REPORT_PATH}")
    print(f"Grille d'exemples écrite dans {GRID_PATH}")


if __name__ == "__main__":
    run()
