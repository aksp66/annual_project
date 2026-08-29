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

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [data-testid="stAppViewContainer"] {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(180deg, #f5f7fb 0%, #eef3ff 100%);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }

        .hero {
            background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 50%, #2563eb 100%);
            border-radius: 1.1rem;
            padding: 1.5rem 1.7rem;
            margin-bottom: 1.25rem;
            box-shadow: 0 10px 30px rgba(37, 99, 235, 0.18);
        }

        .hero h1 {
            font-size: 2.1rem;
            font-weight: 800;
            color: white;
            margin: 0;
            line-height: 1.2;
        }

        .hero p {
            color: rgba(255,255,255,0.85);
            margin: 0.5rem 0 0 0;
            font-size: 1rem;
        }

        [data-testid="stSidebar"] {
            background: rgba(15, 23, 42, 0.96);
            color: #e2e8f0;
        }

        [data-testid="stSidebar"] .st-emotion-cache-1v0mbdj, [data-testid="stSidebar"] .st-emotion-cache-1wyxrv8 {
            background: rgba(148, 163, 184, 0.08);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 0.85rem;
        }

        .card {
            background: rgba(255,255,255,0.9);
            border: 1px solid rgba(148, 163, 184, 0.25);
            border-radius: 0.9rem;
            padding: 1rem 1.1rem;
            box-shadow: 0 8px 18px rgba(15, 23, 42, 0.04);
        }

        .stButton > button {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            color: white;
            border: none;
            border-radius: 0.75rem;
            font-weight: 600;
            padding: 0.6rem 1.1rem;
            transition: all 0.2s ease;
        }

        .stButton > button:hover {
            filter: brightness(1.05);
            box-shadow: 0 8px 18px rgba(37, 99, 235, 0.25);
        }

        .stRadio > div {
            background: rgba(255,255,255,0.7);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 0.8rem;
            padding: 0.4rem 0.5rem;
        }

        .stSlider [data-testid="stBaseSlider"] {
            background: rgba(255,255,255,0.4);
            border-radius: 0.8rem;
        }

        div[data-testid="metric-container"] {
            background: rgba(255,255,255,0.85);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 0.8rem;
            padding: 0.8rem 0.9rem;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.04);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>DDPM vs GAN — Fashion-MNIST</h1>
        <p>Génération visuelle de vêtements par diffusion et réseaux adversariaux.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("<div class='card'><h3 style='margin:0 0 0.5rem 0;'>Informations</h3></div>", unsafe_allow_html=True)
    st.markdown(f"**API** : `{API_URL}`")
    st.markdown("**Modèles** : DDPM, GAN, comparaison")
    st.markdown("**Dataset** : Fashion-MNIST")
    st.markdown("**Objectif** : comparer qualité et vitesse de génération")


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
    col1.metric("FID (référence)", f"{ref['fid']:.1f}")
    col2.metric("Temps requête", f"{elapsed:.2f}s", f"{elapsed / n:.3f}s/image")
    col3.metric("Temps référence / image", f"{ref['gen_time_per_image_s']:.3f}s")


st.markdown("<div class='card'>", unsafe_allow_html=True)
mode = st.radio("Modèle à générer", ["DDPM", "GAN", "Comparaison côte à côte"], horizontal=True)
st.markdown("</div>", unsafe_allow_html=True)

if mode in ("DDPM", "GAN"):
    model = mode.lower()
    n = st.slider("Nombre d'images", 1, MAX_N[model], 1)
    if st.button("Générer", use_container_width=True):
        with st.spinner(f"Génération {mode} en cours..."):
            try:
                data, elapsed = call_generate(model, n)
            except requests.RequestException as exc:
                st.error(f"Erreur API : {exc}")
            else:
                st.markdown("<div class='card'>", unsafe_allow_html=True)
                st.image(decode_images(data["images"]), width=170)
                st.markdown("</div>", unsafe_allow_html=True)
                show_metrics(model, elapsed, n)

else:
    n = st.slider("Nombre d'images par modèle", 1, MAX_N["ddpm"], 1)
    if st.button("Générer côte à côte", use_container_width=True):
        col_ddpm, col_gan = st.columns(2)

        with col_ddpm:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("DDPM")
            with st.spinner("Génération DDPM..."):
                try:
                    data, elapsed = call_generate("ddpm", n)
                except requests.RequestException as exc:
                    st.error(f"Erreur DDPM : {exc}")
                else:
                    st.image(decode_images(data["images"]), width=170)
                    show_metrics("ddpm", elapsed, n)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_gan:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("GAN")
            with st.spinner("Génération GAN..."):
                try:
                    data, elapsed = call_generate("gan", n)
                except requests.RequestException as exc:
                    st.error(f"Erreur GAN : {exc}")
                else:
                    st.image(decode_images(data["images"]), width=170)
                    show_metrics("gan", elapsed, n)
            st.markdown("</div>", unsafe_allow_html=True)

st.caption(
    "Métriques de référence issues de notebooks/06_evaluation_ddpm_vs_gan.ipynb "
    "(100 images/groupe) — cf. HISTORY.md."
)
