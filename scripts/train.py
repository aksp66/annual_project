"""Point d'entrée générique pour lancer un entraînement à partir d'une config.

Détecte automatiquement s'il s'agit d'une config DDPM (`configs/ddpm_*.yaml`,
présence de `timesteps`) ou GAN (`configs/gan_*.yaml`, présence de `model.latent_dim`)
et délègue à `src.training.train_ddpm` ou `src.training.train_gan`.

Usage :
    python scripts/train.py --config configs/ddpm_base.yaml
    python scripts/train.py --config configs/gan_base.yaml
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.data.dataset import load_config


def main(config_path: str) -> None:
    config = load_config(config_path)

    if "timesteps" in config:
        from src.training.train_ddpm import train

        print(f"Config DDPM détectée ({config_path}) — timesteps={config['timesteps']}")
        train(config_path)
    elif "latent_dim" in config.get("model", {}):
        from src.training.train_gan import train

        print(f"Config GAN détectée ({config_path})")
        train(config_path)
    else:
        raise ValueError(
            f"Impossible de déterminer le type de config ({config_path}) : "
            "ni 'timesteps' (DDPM) ni 'model.latent_dim' (GAN) trouvés."
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    main(args.config)
