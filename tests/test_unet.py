import torch

from src.data.dataset import load_config
from src.models.ddpm.diffusion import GaussianDiffusion
from src.models.ddpm.unet import UNet

CONFIG_PATH = "configs/ddpm_base.yaml"


def _build_model_and_diffusion():
    config = load_config(CONFIG_PATH)
    model_config = config["model"]
    model = UNet(
        in_channels=model_config["in_channels"],
        base_channels=model_config["base_channels"],
        channel_mults=tuple(model_config["channel_mults"]),
        num_res_blocks=model_config["num_res_blocks"],
    )
    diffusion = GaussianDiffusion(
        timesteps=config["timesteps"],
        schedule=config["schedule"],
        beta_start=config["beta_start"],
        beta_end=config["beta_end"],
    )
    return model, diffusion


def test_unet_output_shape_matches_input():
    model, diffusion = _build_model_and_diffusion()
    x = torch.randn(4, 1, 32, 32)
    t = torch.randint(0, diffusion.timesteps, (4,))
    out = model(x, t)
    assert out.shape == x.shape


def test_unet_handles_different_batch_and_timesteps():
    model, diffusion = _build_model_and_diffusion()
    for batch_size in (1, 3):
        x = torch.randn(batch_size, 1, 32, 32)
        t = torch.randint(0, diffusion.timesteps, (batch_size,))
        out = model(x, t)
        assert out.shape == x.shape


def test_p_losses_is_scalar_and_finite():
    model, diffusion = _build_model_and_diffusion()
    x0 = torch.randn(4, 1, 32, 32)
    t = torch.randint(0, diffusion.timesteps, (4,))
    loss = diffusion.p_losses(model, x0, t)
    assert loss.dim() == 0
    assert torch.isfinite(loss)


def test_p_sample_single_step_shape():
    model, diffusion = _build_model_and_diffusion()
    x_t = torch.randn(2, 1, 32, 32)
    x_prev = diffusion.p_sample(model, x_t, t=diffusion.timesteps - 1)
    assert x_prev.shape == x_t.shape
    assert torch.isfinite(x_prev).all()


def test_p_sample_loop_runs_and_returns_correct_shape():
    model, diffusion = _build_model_and_diffusion()
    # Peu de pas pour que le test reste rapide : on ne teste ici que la mécanique
    # (shapes, absence de NaN), pas la qualité de génération (modèle non entraîné).
    diffusion.timesteps = 5
    diffusion.betas = diffusion.betas[:5]
    diffusion.alphas = diffusion.alphas[:5]
    diffusion.alphas_cumprod = diffusion.alphas_cumprod[:5]
    diffusion.sqrt_alphas_cumprod = diffusion.sqrt_alphas_cumprod[:5]
    diffusion.sqrt_one_minus_alphas_cumprod = diffusion.sqrt_one_minus_alphas_cumprod[:5]
    diffusion.posterior_variance = diffusion.posterior_variance[:5]

    samples = diffusion.p_sample_loop(model, shape=(2, 1, 32, 32))
    assert samples.shape == (2, 1, 32, 32)
    assert torch.isfinite(samples).all()
