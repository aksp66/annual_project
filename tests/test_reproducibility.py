"""Vérifie qu'un même seed + config reproduit les mêmes résultats d'entraînement
(checklist "Scripts de reproductibilité" de TASKS.md).

Utilise une config volontairement minuscule (peu de timesteps, petit modèle,
peu de steps) pour que le test reste rapide — l'objectif est de vérifier le
comportement déterministe du pipeline, pas la qualité d'un entraînement réel.
"""

import csv
import shutil
from pathlib import Path

import yaml

from src.data.dataset import load_config
from src.training.train_ddpm import train

REPO_ROOT = Path(__file__).resolve().parents[1]


def _make_tiny_ddpm_config(tmp_path: Path, output_dir: str) -> Path:
    config = {
        "timesteps": 5,
        "schedule": "linear",
        "beta_start": 0.0001,
        "beta_end": 0.02,
        "seed": 123,
        "model": {
            "in_channels": 1,
            "base_channels": 8,
            "channel_mults": [1, 2],
            "num_res_blocks": 1,
        },
        "training": {
            "num_steps": 3,
            "lr": 0.0002,
            "log_every": 1,
            "sample_every": 3,
            "checkpoint_every": 3,
            "n_samples": 2,
            "output_dir": output_dir,
        },
    }
    config_path = tmp_path / f"{Path(output_dir).name}.yaml"
    with open(config_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(config, f)
    return config_path


def test_same_seed_and_config_reproduce_same_loss_curve(tmp_path):
    output_a = "experiments/_repro_test_a"
    output_b = "experiments/_repro_test_b"

    config_a = _make_tiny_ddpm_config(tmp_path, output_a)
    config_b = _make_tiny_ddpm_config(tmp_path, output_b)

    try:
        train(str(config_a))
        train(str(config_b))

        def read_losses(output_dir: str) -> list[str]:
            with open(REPO_ROOT / output_dir / "log.csv", encoding="utf-8") as f:
                return [row["loss"] for row in csv.DictReader(f)]

        losses_a = read_losses(output_a)
        losses_b = read_losses(output_b)
        assert len(losses_a) == 3
        assert losses_a == losses_b, "Même seed + config doit produire la même séquence de loss"
    finally:
        shutil.rmtree(REPO_ROOT / output_a, ignore_errors=True)
        shutil.rmtree(REPO_ROOT / output_b, ignore_errors=True)
