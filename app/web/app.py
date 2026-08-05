"""App Streamlit de démonstration DDPM vs GAN (cf. PLANNING.md Phase 3, app/README.md).

Appelle l'API FastAPI (`app/api/main.py`) pour générer des images et les
afficher côte à côte, avec les métriques indicatives issues de l'évaluation
(`notebooks/06_evaluation_ddpm_vs_gan.ipynb`).

Usage :
    uvicorn app.api.main:app &
    streamlit run app/web/app.py
"""

import base64
import io
import os
import time

import requests
import streamlit as st
from PIL import Image

API_URL = os.environ.get("API_URL", "http://localhost:8000")

# Métriques de référence mesurées lors de l'évaluation (100 images/groupe,
# cf. HISTORY.md et notebooks/06_evaluation_ddpm_vs_gan.ipynb) — indicatives,
# pas recalculées à chaque génération (trop coûteux en temps réel).
REFERENCE_METRICS = {
    "ddpm": {"fid": 114.12, "gen_time_per_image_s": 18.54},
    "gan": {"fid": 173.47, "gen_time_per_image_s": 0.0009},
}
MAX_N = {"ddpm": 4, "gan": 16}

st.set_page_config(page_title="DDPM vs GAN — Fashion-MNIST", layout="wide")
st.title("DDPM vs GAN — génération de vêtements (Fashion-MNIST)")
st.caption(f"API : {API_URL}")


def decode_images(images_b64: list[str]) -> list[Image.Image]:
    return [Image.open(io.BytesIO(base64.b64decode(b))) for b in images_b64]


def call_generate(model: str, n: int):
    t0 = time.perf_counter()
    response = requests.get(f"{API_URL}/generate", params={"model": model, "n": n}, timeout=120)
    elapsed = time.perf_counter() - t0
    response.raise_for_status()
    return response.json(), elapsed


def show_metrics(model: str, elapsed: float, n: int) -> None:
    ref = REFERENCE_METRICS[model]
    col1, col2, col3 = st.columns(3)
    col1.metric("FID (référence, vs réel)", f"{ref['fid']:.1f}")
    col2.metric("Temps mesuré (cette requête)", f"{elapsed:.2f}s", f"{elapsed / n:.3f}s/image")
    col3.metric("Temps référence / image", f"{ref['gen_time_per_image_s']:.3f}s")


mode = st.radio("Modèle à générer", ["DDPM", "GAN", "Comparaison côte à côte"], horizontal=True)

if mode in ("DDPM", "GAN"):
    model = mode.lower()
    n = st.slider("Nombre d'images", 1, MAX_N[model], 1)
    if st.button("Générer"):
        with st.spinner(f"Génération {mode} en cours..."):
            try:
                data, elapsed = call_generate(model, n)
            except requests.RequestException as exc:
                st.error(f"Erreur API : {exc}")
            else:
                st.image(decode_images(data["images"]), width=150)
                show_metrics(model, elapsed, n)

else:
    n = st.slider("Nombre d'images par modèle", 1, MAX_N["ddpm"], 1)
    if st.button("Générer côte à côte"):
        col_ddpm, col_gan = st.columns(2)

        with col_ddpm:
            st.subheader("DDPM")
            with st.spinner("Génération DDPM..."):
                try:
                    data, elapsed = call_generate("ddpm", n)
                except requests.RequestException as exc:
                    st.error(f"Erreur DDPM : {exc}")
                else:
                    st.image(decode_images(data["images"]), width=150)
                    show_metrics("ddpm", elapsed, n)

        with col_gan:
            st.subheader("GAN")
            with st.spinner("Génération GAN..."):
                try:
                    data, elapsed = call_generate("gan", n)
                except requests.RequestException as exc:
                    st.error(f"Erreur GAN : {exc}")
                else:
                    st.image(decode_images(data["images"]), width=150)
                    show_metrics("gan", elapsed, n)

st.caption(
    "Métriques de référence issues de notebooks/06_evaluation_ddpm_vs_gan.ipynb "
    "(100 images/groupe) — cf. HISTORY.md."
)
