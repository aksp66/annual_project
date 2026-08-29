from pathlib import Path

import torch
import yaml
from torch.utils.data import DataLoader, random_split
from torchvision import datasets, transforms

REPO_ROOT = Path(__file__).resolve().parents[2]


def load_config(config_path: str | Path) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_transform(config: dict) -> transforms.Compose:
    pad = (config["image_size"] - 28) // 2
    return transforms.Compose(
        [
            transforms.Pad(pad, fill=config["pad_value"]),
            transforms.ToTensor(),
            transforms.Normalize((config["normalize_mean"],), (config["normalize_std"],)),
        ]
    )


def get_dataloaders(config: dict) -> tuple[DataLoader, DataLoader, DataLoader]:
    """Construit les DataLoaders train/val/test à partir d'une config (cf. configs/data.yaml).

    Le split val est prélevé sur le train set officiel ; le test set reste
    réservé à l'évaluation finale (FID, comparaison DDPM vs GAN).
    """
    data_dir = REPO_ROOT / config["data_dir"]
    transform = build_transform(config)

    full_train = datasets.FashionMNIST(data_dir, train=True, download=True, transform=transform)
    test_set = datasets.FashionMNIST(data_dir, train=False, download=True, transform=transform)

    n_val = int(len(full_train) * config["val_split"])
    n_train = len(full_train) - n_val
    generator = torch.Generator().manual_seed(config["seed"])
    train_set, val_set = random_split(full_train, [n_train, n_val], generator=generator)

    loader_kwargs = {"batch_size": config["batch_size"], "num_workers": config["num_workers"]}
    train_loader = DataLoader(train_set, shuffle=True, **loader_kwargs)
    val_loader = DataLoader(val_set, shuffle=False, **loader_kwargs)
    test_loader = DataLoader(test_set, shuffle=False, **loader_kwargs)

    return train_loader, val_loader, test_loader
