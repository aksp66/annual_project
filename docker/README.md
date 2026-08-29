# docker/

Conteneurisation du projet : `api.Dockerfile` (API FastAPI) et `web.Dockerfile` (app Streamlit). Orchestration via `docker-compose.yml` à la racine du repo (services `api` port 8000, `web` port 8501).

Les checkpoints entraînés (`experiments/*_baseline/checkpoints/`) ne sont pas copiés dans les images (non versionnés, trop volumineux) : ils sont montés en volume par `docker-compose.yml`. Il faut donc les avoir générés localement au préalable (`python scripts/train.py --config ...`).

Testé de bout en bout (`docker compose up --build`) — cf. `HISTORY.md` (2026-08-05) pour le détail.
