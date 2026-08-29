"""Entraînement baseline du DCGAN (cf. PLANNING.md Phase 2, configs/gan_base.yaml).

Reproductible : seed fixé, config versionnée, checkpoints + logs + échantillons
sauvegardés régulièrement dans `training.output_dir`. Logue les loss G et D
séparément pour repérer un éventuel mode collapse (cf. TASKS.md).

Usage : python -m src.training.train_gan --config configs/gan_base.yaml
"""

import argparse
import csv
import time
from pathlib import Path

import torch
from torch import nn

from src.data.dataset import get_dataloaders, load_config
from src.models.gan.discriminator import Discriminator
from src.models.gan.generator import Generator
from src.utils.seed import set_seed
from src.utils.viz import save_sample_grid

REPO_ROOT = Path(__file__).resolve().parents[2]


def weights_init(module: nn.Module) -> None:
    """Init DCGAN standard (Radford et al. 2015) : poids ~ N(0, 0.02)."""
    classname = module.__class__.__name__
    if "Conv" in classname:
        nn.init.normal_(module.weight.data, 0.0, 0.02)
    elif "BatchNorm" in classname:
        nn.init.normal_(module.weight.data, 1.0, 0.02)
        nn.init.constant_(module.bias.data, 0)


def build_models(gan_config: dict) -> tuple[Generator, Discriminator]:
    mc = gan_config["model"]
    generator = Generator(latent_dim=mc["latent_dim"], base_channels=mc["base_channels"], out_channels=mc["out_channels"])
    discriminator = Discriminator(base_channels=mc["base_channels"], in_channels=mc["out_channels"])
    generator.apply(weights_init)
    discriminator.apply(weights_init)
    return generator, discriminator


def train(gan_config_path: str, data_config_path: str = "configs/data.yaml") -> None:
    gan_config = load_config(REPO_ROOT / gan_config_path)
    data_config = load_config(REPO_ROOT / data_config_path)
    train_cfg = gan_config["training"]
    latent_dim = gan_config["model"]["latent_dim"]

    set_seed(gan_config["seed"])

    output_dir = REPO_ROOT / train_cfg["output_dir"]
    checkpoints_dir = output_dir / "checkpoints"
    samples_dir = output_dir / "samples"
    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    samples_dir.mkdir(parents=True, exist_ok=True)
    log_path = output_dir / "log.csv"

    generator, discriminator = build_models(gan_config)
    criterion = nn.BCEWithLogitsLoss()
    opt_g = torch.optim.Adam(generator.parameters(), lr=train_cfg["lr"], betas=(train_cfg["beta1"], train_cfg["beta2"]))
    opt_d = torch.optim.Adam(
        discriminator.parameters(), lr=train_cfg["lr"], betas=(train_cfg["beta1"], train_cfg["beta2"])
    )

    train_loader, _, _ = get_dataloaders(data_config)
    data_iter = iter(train_loader)

    with open(log_path, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(["step", "loss_d", "loss_g", "d_real_mean", "d_fake_mean", "elapsed_s"])

    fixed_noise = torch.randn(train_cfg["n_samples"], latent_dim, 1, 1)

    t_start = time.perf_counter()
    for step in range(1, train_cfg["num_steps"] + 1):
        try:
            real, _ = next(data_iter)
        except StopIteration:
            data_iter = iter(train_loader)
            real, _ = next(data_iter)

        batch_size = real.shape[0]
        real_labels = torch.ones(batch_size)
        fake_labels = torch.zeros(batch_size)

        # --- Discriminateur : maximiser log(D(real)) + log(1 - D(G(z))) ---
        noise = torch.randn(batch_size, latent_dim, 1, 1)
        fake = generator(noise)

        opt_d.zero_grad()
        d_real_logits = discriminator(real)
        loss_d_real = criterion(d_real_logits, real_labels)
        d_fake_logits = discriminator(fake.detach())
        loss_d_fake = criterion(d_fake_logits, fake_labels)
        loss_d = loss_d_real + loss_d_fake
        loss_d.backward()
        opt_d.step()

        # --- Générateur : maximiser log(D(G(z))) ---
        opt_g.zero_grad()
        d_fake_logits_for_g = discriminator(fake)
        loss_g = criterion(d_fake_logits_for_g, real_labels)
        loss_g.backward()
        opt_g.step()

        if step % train_cfg["log_every"] == 0 or step == 1:
            elapsed = time.perf_counter() - t_start
            d_real_mean = torch.sigmoid(d_real_logits).mean().item()
            d_fake_mean = torch.sigmoid(d_fake_logits).mean().item()
            with open(log_path, "a", newline="", encoding="utf-8") as f:
                csv.writer(f).writerow(
                    [step, loss_d.item(), loss_g.item(), d_real_mean, d_fake_mean, round(elapsed, 2)]
                )
            print(
                f"step {step:5d}/{train_cfg['num_steps']} — loss_d={loss_d.item():.4f} "
                f"loss_g={loss_g.item():.4f} D(real)={d_real_mean:.2f} D(fake)={d_fake_mean:.2f} — {elapsed:.0f}s"
            )

        if step % train_cfg["checkpoint_every"] == 0 or step == train_cfg["num_steps"]:
            torch.save(
                {
                    "step": step,
                    "generator_state_dict": generator.state_dict(),
                    "discriminator_state_dict": discriminator.state_dict(),
                    "config": gan_config,
                },
                checkpoints_dir / f"gan_step{step:06d}.pt",
            )

        if step % train_cfg["sample_every"] == 0 or step == train_cfg["num_steps"]:
            generator.eval()
            with torch.no_grad():
                samples = generator(fixed_noise)
            save_sample_grid(samples, samples_dir / f"step_{step:06d}.png", nrow=4)
            generator.train()

    print(f"Entraînement terminé en {time.perf_counter() - t_start:.0f}s. Sorties dans {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/gan_base.yaml")
    args = parser.parse_args()
    train(args.config)
