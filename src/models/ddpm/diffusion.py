import math

import torch
import torch.nn.functional as F


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

        # Processus inverse : variance a posteriori q(x_{t-1} | x_t, x_0) (Ho et al. 2020, eq. 7).
        alphas_cumprod_prev = F.pad(self.alphas_cumprod[:-1], (1, 0), value=1.0)
        self.posterior_variance = self.betas * (1.0 - alphas_cumprod_prev) / (1.0 - self.alphas_cumprod)

    def _extract(self, values: torch.Tensor, t: torch.Tensor, x_shape: torch.Size) -> torch.Tensor:
        shape = (-1,) + (1,) * (len(x_shape) - 1)
        return values.to(t.device)[t].view(*shape)

    def q_sample(self, x0: torch.Tensor, t: torch.Tensor, noise: torch.Tensor | None = None) -> torch.Tensor:
        """q(x_t | x_0) = sqrt(alphas_cumprod_t) * x_0 + sqrt(1 - alphas_cumprod_t) * noise."""
        if noise is None:
            noise = torch.randn_like(x0)
        sqrt_ac = self._extract(self.sqrt_alphas_cumprod, t, x0.shape)
        sqrt_1m_ac = self._extract(self.sqrt_one_minus_alphas_cumprod, t, x0.shape)
        return sqrt_ac * x0 + sqrt_1m_ac * noise

    def p_losses(self, model: torch.nn.Module, x0: torch.Tensor, t: torch.Tensor) -> torch.Tensor:
        """Loss d'entraînement : MSE entre le bruit réel et le bruit prédit par le U-Net."""
        noise = torch.randn_like(x0)
        x_t = self.q_sample(x0, t, noise=noise)
        predicted_noise = model(x_t, t)
        return F.mse_loss(predicted_noise, noise)

    @torch.no_grad()
    def p_sample(self, model: torch.nn.Module, x_t: torch.Tensor, t: int) -> torch.Tensor:
        """Un pas du processus inverse p(x_{t-1} | x_t) — sampling ancestral."""
        t_batch = torch.full((x_t.shape[0],), t, device=x_t.device, dtype=torch.long)
        beta_t = self._extract(self.betas, t_batch, x_t.shape)
        sqrt_1m_ac = self._extract(self.sqrt_one_minus_alphas_cumprod, t_batch, x_t.shape)
        sqrt_recip_alpha = self._extract(1.0 / torch.sqrt(self.alphas), t_batch, x_t.shape)

        predicted_noise = model(x_t, t_batch)
        mean = sqrt_recip_alpha * (x_t - beta_t / sqrt_1m_ac * predicted_noise)

        if t == 0:
            return mean
        variance = self._extract(self.posterior_variance, t_batch, x_t.shape)
        return mean + torch.sqrt(variance) * torch.randn_like(x_t)

    @torch.no_grad()
    def p_sample_loop(
        self, model: torch.nn.Module, shape: tuple[int, ...], device: str | torch.device = "cpu"
    ) -> torch.Tensor:
        """Boucle d'échantillonnage complète x_T (bruit pur) -> x_0."""
        model.eval()
        x_t = torch.randn(shape, device=device)
        for t in reversed(range(self.timesteps)):
            x_t = self.p_sample(model, x_t, t)
        return x_t
