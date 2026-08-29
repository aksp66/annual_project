import torch
from torch import nn

from src.data.dataset import load_config
from src.models.gan.discriminator import Discriminator
from src.models.gan.generator import Generator

CONFIG_PATH = "configs/gan_base.yaml"


def _build_models():
    config = load_config(CONFIG_PATH)
    mc = config["model"]
    generator = Generator(latent_dim=mc["latent_dim"], base_channels=mc["base_channels"], out_channels=mc["out_channels"])
    discriminator = Discriminator(base_channels=mc["base_channels"], in_channels=mc["out_channels"])
    return config, generator, discriminator


def test_generator_output_shape_and_range():
    config, generator, _ = _build_models()
    latent_dim = config["model"]["latent_dim"]
    z = torch.randn(4, latent_dim, 1, 1)
    fake = generator(z)
    assert fake.shape == (4, 1, 32, 32)
    assert fake.min() >= -1.0 - 1e-5
    assert fake.max() <= 1.0 + 1e-5


def test_discriminator_output_shape():
    _, _, discriminator = _build_models()
    x = torch.randn(4, 1, 32, 32)
    out = discriminator(x)
    assert out.shape == (4,)


def test_generator_discriminator_pipeline():
    config, generator, discriminator = _build_models()
    latent_dim = config["model"]["latent_dim"]
    z = torch.randn(6, latent_dim, 1, 1)
    fake = generator(z)
    logits = discriminator(fake)
    assert logits.shape == (6,)
    assert torch.isfinite(logits).all()


def test_bce_loss_and_backward_pass():
    config, generator, discriminator = _build_models()
    latent_dim = config["model"]["latent_dim"]
    criterion = nn.BCEWithLogitsLoss()

    z = torch.randn(4, latent_dim, 1, 1)
    fake = generator(z)
    logits = discriminator(fake)
    labels = torch.ones(4)
    loss = criterion(logits, labels)

    loss.backward()
    grad_norms = [p.grad.abs().sum().item() for p in generator.parameters() if p.grad is not None]
    assert len(grad_norms) > 0
    assert all(g >= 0 for g in grad_norms)


def test_adam_optimizers_betas_from_config():
    config, generator, discriminator = _build_models()
    train_cfg = config["training"]
    opt_g = torch.optim.Adam(generator.parameters(), lr=train_cfg["lr"], betas=(train_cfg["beta1"], train_cfg["beta2"]))
    assert opt_g.param_groups[0]["betas"] == (0.5, 0.999)
