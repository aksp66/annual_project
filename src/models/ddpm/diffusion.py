import math

import torch


def make_beta_schedule(
    schedule: str, timesteps: int, beta_start: float = 1e-4, beta_end: float = 0.02
) -> torch.Tensor:
    if schedule == "linear":
        return torch.linspace(beta_start, beta_end, timesteps)
    if schedule == "cosine":
        # Nichol & Dhariwal 2021 - https://arxiv.org/abs/2102.09672
        s = 0.008
        steps = timesteps + 1
        t = torch.linspace(0, timesteps, steps) / timesteps
        alphas_cumprod = torch.cos((t + s) / (1 + s) * math.pi / 2) ** 2
        alphas_cumprod = alphas_cumprod / alphas_cumprod[0]
        betas = 1.0 - (alphas_cumprod[1:] / alphas_cumprod[:-1])
        return torch.clip(betas, 1e-4, 0.9999)
    raise ValueError(f"Schedule de bruit inconnu : {schedule!r} (attendu : 'linear' ou 'cosine')")


class GaussianDiffusion:
    """Processus de diffusion direct (forward), from scratch (Ho et al. 2020).

    Bruitage x_0 -> x_t via la formule fermée q(x_t | x_0), sans boucle sur les
    pas intermédiaires.
    """

    def __init__(
        self, timesteps: int, schedule: str = "linear", beta_start: float = 1e-4, beta_end: float = 0.02
    ):
        self.timesteps = timesteps
        self.betas = make_beta_schedule(schedule, timesteps, beta_start, beta_end)
        self.alphas = 1.0 - self.betas
        self.alphas_cumprod = torch.cumprod(self.alphas, dim=0)
        self.sqrt_alphas_cumprod = torch.sqrt(self.alphas_cumprod)
        self.sqrt_one_minus_alphas_cumprod = torch.sqrt(1.0 - self.alphas_cumprod)

    def q_sample(self, x0: torch.Tensor, t: torch.Tensor, noise: torch.Tensor | None = None) -> torch.Tensor:
        """q(x_t | x_0) = sqrt(alphas_cumprod_t) * x_0 + sqrt(1 - alphas_cumprod_t) * noise."""
        if noise is None:
            noise = torch.randn_like(x0)
        shape = (-1,) + (1,) * (x0.dim() - 1)
        sqrt_ac = self.sqrt_alphas_cumprod.to(x0.device)[t].view(*shape)
        sqrt_1m_ac = self.sqrt_one_minus_alphas_cumprod.to(x0.device)[t].view(*shape)
        return sqrt_ac * x0 + sqrt_1m_ac * noise
