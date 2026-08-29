import torch

from src.data.dataset import load_config
from src.models.ddpm.diffusion import GaussianDiffusion, make_beta_schedule

CONFIG_PATH = "configs/ddpm_base.yaml"


def _load_diffusion():
    config = load_config(CONFIG_PATH)
    diffusion = GaussianDiffusion(
        timesteps=config["timesteps"],
        schedule=config["schedule"],
        beta_start=config["beta_start"],
        beta_end=config["beta_end"],
    )
    return config, diffusion


def test_beta_schedule_shape_and_bounds():
    config, diffusion = _load_diffusion()
    assert diffusion.betas.shape == (config["timesteps"],)
    assert torch.all(diffusion.betas >= config["beta_start"] - 1e-6)
    assert torch.all(diffusion.betas <= config["beta_end"] + 1e-6)
    assert torch.all(diffusion.alphas_cumprod[1:] < diffusion.alphas_cumprod[:-1])  # décroissant


def test_cosine_schedule_runs():
    betas = make_beta_schedule("cosine", timesteps=1000)
    assert betas.shape == (1000,)
    assert torch.all(betas > 0) and torch.all(betas < 1)


def test_q_sample_shape():
    _, diffusion = _load_diffusion()
    torch.manual_seed(0)
    x0 = torch.randn(8, 1, 32, 32)
    t = torch.randint(0, diffusion.timesteps, (8,))
    x_t = diffusion.q_sample(x0, t)
    assert x_t.shape == x0.shape


def test_q_sample_at_t0_close_to_x0():
    _, diffusion = _load_diffusion()
    torch.manual_seed(0)
    x0 = torch.randn(4, 1, 32, 32)
    t = torch.zeros(4, dtype=torch.long)
    noise = torch.randn_like(x0)
    x_t = diffusion.q_sample(x0, t, noise=noise)
    # A t=0, beta_start est très petit : x_t doit rester très proche de x0.
    assert torch.allclose(x_t, x0, atol=0.1)


def test_noise_increases_with_t():
    _, diffusion = _load_diffusion()
    torch.manual_seed(0)
    x0 = torch.zeros(1, 1, 32, 32)
    noise = torch.randn_like(x0)
    early = diffusion.q_sample(x0, torch.tensor([10]), noise=noise)
    late = diffusion.q_sample(x0, torch.tensor([900]), noise=noise)
    assert late.abs().mean() > early.abs().mean()


def test_x_T_close_to_standard_gaussian():
    _, diffusion = _load_diffusion()
    torch.manual_seed(0)
    x0 = torch.randn(2000, 1, 32, 32)  # imite des images normalisées dans [-1, 1]
    t = torch.full((2000,), diffusion.timesteps - 1, dtype=torch.long)
    x_T = diffusion.q_sample(x0, t)
    assert abs(x_T.mean().item()) < 0.05
    assert abs(x_T.std().item() - 1.0) < 0.05
