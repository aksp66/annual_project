"""
Compare les datasets candidats (Fashion-MNIST vs CIFAR-10) pour le choix
de la Phase 1 (cf. PLANNING.md / TASKS.md).

Télécharge les deux datasets via torchvision.datasets dans data/raw/,
vérifie le chargement local et affiche un tableau comparatif (volume,
résolution, canaux, classes, poids sur disque, temps de chargement).

Usage: python scripts/compare_datasets.py
"""

import time
from pathlib import Path

import torch
from torchvision import datasets, transforms

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


def describe(name, train_ds, test_ds, root):
    x0, y0 = train_ds[0]
    tensor = transforms.ToTensor()(x0) if not torch.is_tensor(x0) else x0
    size_bytes = sum(f.stat().st_size for f in root.rglob("*") if f.is_file())
    classes = getattr(train_ds, "classes", None)
    n_classes = len(classes) if classes else len(set(train_ds.targets.tolist() if torch.is_tensor(train_ds.targets) else train_ds.targets))

    return {
        "name": name,
        "n_train": len(train_ds),
        "n_test": len(test_ds),
        "image_size": tuple(tensor.shape),
        "n_classes": n_classes,
        "disk_mb": round(size_bytes / (1024 * 1024), 2),
    }


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    to_tensor = transforms.ToTensor()

    print("Téléchargement / chargement de Fashion-MNIST...")
    t0 = time.perf_counter()
    fmnist_train = datasets.FashionMNIST(DATA_DIR, train=True, download=True, transform=to_tensor)
    fmnist_test = datasets.FashionMNIST(DATA_DIR, train=False, download=True, transform=to_tensor)
    fmnist_load_s = time.perf_counter() - t0

    print("Téléchargement / chargement de CIFAR-10...")
    t0 = time.perf_counter()
    cifar_train = datasets.CIFAR10(DATA_DIR, train=True, download=True, transform=to_tensor)
    cifar_test = datasets.CIFAR10(DATA_DIR, train=False, download=True, transform=to_tensor)
    cifar_load_s = time.perf_counter() - t0

    fmnist = describe("Fashion-MNIST", fmnist_train, fmnist_test, DATA_DIR / "FashionMNIST")
    fmnist["load_s"] = round(fmnist_load_s, 2)
    cifar = describe("CIFAR-10", cifar_train, cifar_test, DATA_DIR / "cifar-10-batches-py")
    cifar["load_s"] = round(cifar_load_s, 2)

    # Vérification rapide du DataLoader (shape/plage de valeurs en sortie)
    for ds, info in ((fmnist_train, fmnist), (cifar_train, cifar)):
        loader = torch.utils.data.DataLoader(ds, batch_size=8, shuffle=True)
        batch_x, batch_y = next(iter(loader))
        info["batch_shape"] = tuple(batch_x.shape)
        info["pixel_min"] = round(batch_x.min().item(), 3)
        info["pixel_max"] = round(batch_x.max().item(), 3)

    print("\n=== Comparatif ===")
    header = f"{'':16}{'train':>8}{'test':>8}{'taille img':>14}{'classes':>9}{'disque (Mo)':>13}{'chargement (s)':>16}"
    print(header)
    for info in (fmnist, cifar):
        print(
            f"{info['name']:16}{info['n_train']:>8}{info['n_test']:>8}"
            f"{str(info['image_size']):>14}{info['n_classes']:>9}"
            f"{info['disk_mb']:>13}{info['load_s']:>16}"
        )

    print("\nBatch check (DataLoader, batch_size=8):")
    for info in (fmnist, cifar):
        print(f"  {info['name']:16} shape={info['batch_shape']} pixels=[{info['pixel_min']}, {info['pixel_max']}]")

    # Estimation grossière du coût relatif d'entraînement par image
    # (proportionnel au nombre de pixels x canaux, U-Net/DCGAN scaling ~O(pixels))
    fmnist_pixels = fmnist["image_size"][1] * fmnist["image_size"][2] * fmnist["image_size"][0]
    cifar_pixels = cifar["image_size"][1] * cifar["image_size"][2] * cifar["image_size"][0]
    ratio = cifar_pixels / fmnist_pixels
    print(f"\nRatio de pixels/canaux CIFAR-10 vs Fashion-MNIST : x{ratio:.2f}")
    print(f"CUDA disponible : {torch.cuda.is_available()}")


if __name__ == "__main__":
    main()
