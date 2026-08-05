"""API FastAPI de génération DDPM/GAN (cf. PLANNING.md Phase 3, app/README.md).

Charge les deux modèles baseline une fois au démarrage, expose un endpoint de
génération commun aux deux.

Usage : uvicorn app.api.main:app --reload
"""

import base64
import io
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

import torch
from fastapi import FastAPI, HTTPException, Query
from PIL import Image

from src.data.dataset import load_config
from src.models.ddpm.diffusion import GaussianDiffusion
from src.models.ddpm.unet import UNet
from src.models.gan.generator import Generator

REPO_ROOT = Path(__file__).resolve().parents[2]

# Génération DDPM coûteuse en CPU (~18s/image, cf. HISTORY.md) : on plafonne
# le nombre d'images par requête pour garder l'API réactive.
MAX_N_DDPM = 4
MAX_N_GAN = 16

models: dict = {}


def load_models() -> None:
    ddpm_config = load_config(REPO_ROOT / "configs" / "ddpm_base.yaml")
    ddpm_checkpoint_path = REPO_ROOT / "experiments" / "ddpm_baseline" / "checkpoints" / "ddpm_step001000.pt"
    if ddpm_checkpoint_path.exists():
        mc = ddpm_config["model"]
        ddpm_model = UNet(
            in_channels=mc["in_channels"],
            base_channels=mc["base_channels"],
            channel_mults=tuple(mc["channel_mults"]),
            num_res_blocks=mc["num_res_blocks"],
        )
        checkpoint = torch.load(ddpm_checkpoint_path, map_location="cpu", weights_only=False)
        ddpm_model.load_state_dict(checkpoint["model_state_dict"])
        ddpm_model.eval()
        models["ddpm_model"] = ddpm_model
        models["diffusion"] = GaussianDiffusion(
            timesteps=ddpm_config["timesteps"],
            schedule=ddpm_config["schedule"],
            beta_start=ddpm_config["beta_start"],
            beta_end=ddpm_config["beta_end"],
        )

    gan_config = load_config(REPO_ROOT / "configs" / "gan_base.yaml")
    gan_checkpoint_path = REPO_ROOT / "experiments" / "gan_baseline" / "checkpoints" / "gan_step001000.pt"
    if gan_checkpoint_path.exists():
        gmc = gan_config["model"]
        generator = Generator(latent_dim=gmc["latent_dim"], base_channels=gmc["base_channels"], out_channels=gmc["out_channels"])
        checkpoint = torch.load(gan_checkpoint_path, map_location="cpu", weights_only=False)
        generator.load_state_dict(checkpoint["generator_state_dict"])
        generator.eval()
        models["gan_generator"] = generator
        models["latent_dim"] = gmc["latent_dim"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_models()
    yield
    models.clear()


app = FastAPI(title="DDPM vs GAN — API de génération", lifespan=lifespan)


def tensor_to_base64_png(image_tensor: torch.Tensor) -> str:
    array = ((image_tensor.clamp(-1, 1) + 1) / 2 * 255).byte().squeeze(0).cpu().numpy()
    pil_image = Image.fromarray(array, mode="L")
    buffer = io.BytesIO()
    pil_image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "models_loaded": sorted(models.keys())}


@app.get("/generate")
def generate(model: Literal["ddpm", "gan"] = Query(...), n: int = Query(1, ge=1)) -> dict:
    if model == "ddpm":
        if "ddpm_model" not in models:
            raise HTTPException(status_code=503, detail="Modèle DDPM non chargé (checkpoint introuvable)")
        if n > MAX_N_DDPM:
            raise HTTPException(status_code=400, detail=f"n trop grand pour DDPM (max {MAX_N_DDPM})")
        with torch.no_grad():
            images = models["diffusion"].p_sample_loop(models["ddpm_model"], shape=(n, 1, 32, 32))
    else:
        if "gan_generator" not in models:
            raise HTTPException(status_code=503, detail="Modèle GAN non chargé (checkpoint introuvable)")
        if n > MAX_N_GAN:
            raise HTTPException(status_code=400, detail=f"n trop grand pour GAN (max {MAX_N_GAN})")
        with torch.no_grad():
            noise = torch.randn(n, models["latent_dim"], 1, 1)
            images = models["gan_generator"](noise)

    return {"model": model, "n": n, "images": [tensor_to_base64_png(images[i]) for i in range(n)]}
