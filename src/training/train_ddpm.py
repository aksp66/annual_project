"""Entraînement baseline du DDPM (cf. PLANNING.md Phase 2, configs/ddpm_base.yaml).

Reproductible : seed fixé, config versionnée, checkpoints + logs + échantillons
sauvegardés régulièrement dans `training.output_dir`.

Usage : python -m src.training.train_ddpm --config configs/ddpm_base.yaml
"""

import argparse
import csv
import json
import time
from pathlib import Path

import torch

from src.data.dataset import get_dataloaders, load_config
from src.models.ddpm.diffusion import GaussianDiffusion
from src.models.ddpm.unet import UNet
from src.utils.seed import set_seed
from src.utils.viz import save_sample_grid

REPO_ROOT = Path(__file__).resolve().parents[2]


def build_model_and_diffusion(ddpm_config: dict) -> tuple[UNet, GaussianDiffusion]:
    mc = ddpm_config["model"]
    model = UNet(
        in_channels=mc["in_channels"],
        base_channels=mc["base_channels"],
        channel_mults=tuple(mc["channel_mults"]),
        num_res_blocks=mc["num_res_blocks"],
    )
    diffusion = GaussianDiffusion(
        timesteps=ddpm_config["timesteps"],
        schedule=ddpm_config["schedule"],
        beta_start=ddpm_config["beta_start"],
        beta_end=ddpm_config["beta_end"],
    )
    return model, diffusion


def train(ddpm_config_path: str, data_config_path: str = "configs/data.yaml") -> None:
    ddpm_config = load_config(REPO_ROOT / ddpm_config_path)
    data_config = load_config(REPO_ROOT / data_config_path)
    train_cfg = ddpm_config["training"]

    set_seed(ddpm_config["seed"])

    output_dir = REPO_ROOT / train_cfg["output_dir"]
    checkpoints_dir = output_dir / "checkpoints"
    samples_dir = output_dir / "samples"
    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    samples_dir.mkdir(parents=True, exist_ok=True)
    log_path = output_dir / "log.csv"

    model, diffusion = build_model_and_diffusion(ddpm_config)
    optimizer = torch.optim.Adam(model.parameters(), lr=train_cfg["lr"])

    train_loader, _, _ = get_dataloaders(data_config)
    data_iter = iter(train_loader)

    with open(log_path, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(["step", "loss", "elapsed_s"])

    recent_losses = []
    t_start = time.perf_counter()
    for step in range(1, train_cfg["num_steps"] + 1):
        try:
            x0, _ = next(data_iter)
        except StopIteration:
            data_iter = iter(train_loader)
            x0, _ = next(data_iter)

        t = torch.randint(0, diffusion.timesteps, (x0.shape[0],))
        loss = diffusion.p_losses(model, x0, t)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        recent_losses.append(loss.item())
        recent_losses = recent_losses[-20:]

        if step % train_cfg["log_every"] == 0 or step == 1:
            elapsed = time.perf_counter() - t_start
            with open(log_path, "a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow([step, loss.item(), round(elapsed, 2)])
            print(f"step {step:5d}/{train_cfg['num_steps']} — loss={loss.item():.4f} — {elapsed:.0f}s")

        if step % train_cfg["checkpoint_every"] == 0 or step == train_cfg["num_steps"]:
            torch.save(
                {"step": step, "model_state_dict": model.state_dict(), "config": ddpm_config},
                checkpoints_dir / f"ddpm_step{step:06d}.pt",
            )

        if step % train_cfg["sample_every"] == 0 or step == train_cfg["num_steps"]:
            image_size = data_config["image_size"]
            samples = diffusion.p_sample_loop(
                model, shape=(train_cfg["n_samples"], 1, image_size, image_size)
            )
            save_sample_grid(samples, samples_dir / f"step_{step:06d}.png", nrow=4)
            model.train()

    total_train_time_s = time.perf_counter() - t_start

    # Mesure isolée du temps de génération (hors entraînement), pour l'étude d'ablation
    # sur le nombre de pas de diffusion (cf. TASKS.md).
    image_size = data_config["image_size"]
    t_gen = time.perf_counter()
    diffusion.p_sample_loop(model, shape=(train_cfg["n_samples"], 1, image_size, image_size))
    generation_time_s = time.perf_counter() - t_gen

    summary = {
        "config": str(ddpm_config_path),
        "timesteps": diffusion.timesteps,
        "num_train_steps": train_cfg["num_steps"],
        "total_train_time_s": round(total_train_time_s, 2),
        "final_loss_avg_last20": round(sum(recent_losses) / len(recent_losses), 4),
        "generation_time_s": round(generation_time_s, 2),
        "n_samples_generated": train_cfg["n_samples"],
    }
    with open(output_dir / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(f"Entraînement terminé en {total_train_time_s:.0f}s. Génération ({train_cfg['n_samples']} images) : {generation_time_s:.1f}s. Sorties dans {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/ddpm_base.yaml")
    args = parser.parse_args()
    train(args.config)
