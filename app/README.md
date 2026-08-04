# app/

Application de démonstration : génération d'images côte à côte par le DDPM et le GAN entraînés.

- `api/` — API (FastAPI) qui charge les deux modèles et expose un endpoint de génération.
- `web/` — interface (Streamlit) qui appelle l'API et affiche les résultats.

Exigence allégée niveau Master : l'app sert à illustrer les résultats du rapport, pas à être un produit fini.
