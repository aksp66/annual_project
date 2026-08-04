from pathlib import Path

import torch
from torchvision.utils import make_grid, save_image


def save_sample_grid(images: torch.Tensor, path: str | Path, nrow: int = 8) -> None:
    """Sauvegarde une grille d'images générées (dénormalise [-1, 1] -> [0, 1])."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    images = (images.clamp(-1, 1) + 1) / 2
    grid = make_grid(images, nrow=nrow)
    save_image(grid, path)
