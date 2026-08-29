"""Métriques d'évaluation et de comparaison DDPM vs GAN (cf. TASKS.md).

- FID (Fréchet Inception Distance), via torchmetrics/torch-fidelity.
- Diversité des échantillons (variance intra-batch, doublons quasi-identiques).
"""

import torch
from torchmetrics.image.fid import FrechetInceptionDistance


def to_fid_input(images: torch.Tensor) -> torch.Tensor:
    """Convertit des images normalisées [-1, 1], 1 canal, vers [0, 1], 3 canaux (attendu par Inception)."""
    images = (images.clamp(-1, 1) + 1) / 2
    return images.repeat(1, 3, 1, 1)


def compute_fid(real_images: torch.Tensor, fake_images: torch.Tensor) -> float:
    """FID entre un jeu d'images réelles et un jeu d'images générées (mêmes conventions : [-1,1], 1 canal)."""
    fid = FrechetInceptionDistance(feature=2048, normalize=True)
    fid.update(to_fid_input(real_images), real=True)
    fid.update(to_fid_input(fake_images), real=False)
    return fid.compute().item()


def pixel_variance(images: torch.Tensor) -> float:
    """Variance intra-batch moyenne, pixel par pixel — proxy simple de diversité."""
    return images.var(dim=0).mean().item()


def count_near_duplicate_pairs(images: torch.Tensor, threshold: float = 0.05) -> int:
    """Nombre de paires d'images quasi-identiques (distance euclidienne normalisée < threshold)."""
    n = images.shape[0]
    flat = images.view(n, -1)
    dists = torch.cdist(flat, flat) / flat.shape[1] ** 0.5
    upper_triangle = torch.triu(torch.ones(n, n, dtype=torch.bool), diagonal=1)
    return int(((dists < threshold) & upper_triangle).sum().item())
