"""Télécharge et prépare le dataset Fashion-MNIST (cf. configs/data.yaml).

Usage : python scripts/prepare_data.py [--config configs/data.yaml]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data.dataset import get_dataloaders, load_config


def main(config_path: str) -> None:
    config = load_config(config_path)
    train_loader, val_loader, test_loader = get_dataloaders(config)
    print(f"Dataset       : {config['dataset']}")
    print(f"Train / Val   : {len(train_loader.dataset)} / {len(val_loader.dataset)} images")
    print(f"Test          : {len(test_loader.dataset)} images")
    print(f"Répertoire    : {Path(config['data_dir']).resolve()}")

    batch_x, batch_y = next(iter(train_loader))
    print(f"Batch shape   : {tuple(batch_x.shape)}, pixels dans [{batch_x.min():.2f}, {batch_x.max():.2f}]")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/data.yaml")
    args = parser.parse_args()
    main(args.config)
