# Diffusion (DDPM) from scratch vs. GAN

Projet annuel — cours *Projets AI & Big Data* (TCHAYE-KONDI Jude, Ph.D.), Master.

Implémentation from scratch d'un modèle de diffusion débruitant (DDPM) et comparaison rigoureuse à un GAN (DCGAN) entraîné sur le même dataset et un budget de calcul comparable : qualité de génération, diversité des échantillons, stabilité d'entraînement, coût de calcul.

## Équipe

|Nom|Rôle|
|---|---|
|KOYE Leleda Ma Belle (`Mabelle95`)|Data / Experiment Engineer|
|AHLI Kossi Sitsofe Pédro|Model / Research Engineer (principal), appui Reporting / Backend Developer|
|KONTEVI Akossiwa Anne (`anne952`)|Reporting / Backend Developer|

## Sujet

- Processus de diffusion direct (bruitage) et inverse (débruitage appris par un petit U-Net), implémenté from scratch.
- DCGAN entraîné sur le même dataset, budget comparable.
- Étude d'ablation : nombre de pas de diffusion (ex. 100 vs 1000) — effet sur qualité vs temps de génération.
- Comparaison chiffrée DDPM vs GAN (FID ou évaluation qualitative structurée, diversité des échantillons).
- Analyse de la stabilité d'entraînement (GAN vs DDPM).

Détails complets du sujet : [`project/projets_master.md`](project/projets_master.md) (sujet n°3).

## Structure du repo

```text
.
├── src/                # code source (data, models/ddpm, models/gan, training, evaluation, utils)
├── data/                # données (non versionnées) : raw/, processed/
├── notebooks/           # EDA, prototypage
├── configs/             # une config YAML par expérience (base de l'étude d'ablation)
├── experiments/         # sorties d'entraînement (non versionnées) : checkpoints, logs, échantillons
├── app/                 # démo : api/ (FastAPI) + web/ (Streamlit)
├── docker/              # conteneurisation
├── presentation/         # trame de soutenance et scénario de démo
├── reports/             # rapport final (style article scientifique)
├── scripts/             # scripts de reproduction des résultats
├── tests/               # tests unitaires
├── project/             # documents de cadrage du cours (slides, modalités)
└── HISTORY.md           # journal chronologique du travail
```

Chaque dossier contient un `README.md` détaillant son contenu.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate   # ou .venv\Scripts\activate sous Windows
pip install -r requirements.txt
```

## Démo (API + app)

```bash
docker compose up --build
```

|Service|Port|Variable d'environnement|
|---|---|---|
|`api` (FastAPI)|[localhost:8000](http://localhost:8000) (`/health`, `/generate?model=ddpm\|gan&n=...`)|—|
|`web` (Streamlit)|[localhost:8501](http://localhost:8501)|`API_URL` (défaut : `http://localhost:8000`, réglé sur `http://api:8000` dans `docker-compose.yml`)|

Les checkpoints entraînés (`experiments/*_baseline/checkpoints/`, non versionnés — voir `.gitignore`) sont montés en volume dans le conteneur `api` : il faut donc avoir entraîné au moins une fois les modèles baseline en local avant de lancer la démo (`python scripts/train.py --config configs/ddpm_base.yaml`, puis `configs/gan_base.yaml`). Sans checkpoint, l'API démarre quand même mais renvoie une erreur 503 sur l'endpoint concerné.

Sans Docker : `uvicorn app.api.main:app --port 8000` puis `API_URL=http://localhost:8000 streamlit run app/web/app.py`.

## Planning

Découpage du travail par phase, tâche, rôle et durée estimée : voir [`PLANNING.md`](PLANNING.md).
Détail des actions concrètes par rôle et fonctionnalité : voir [`TASKS.md`](TASKS.md).

## Contribuer

Convention de branches et workflow de PR : voir [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Suivi du projet

L'avancement (décisions, actions, résultats) est journalisé dans [`HISTORY.md`](HISTORY.md).

## Livrables attendus

- Rapport PDF (8-20 pages, style article scientifique) — envoyé à <tchaye59@gmail.com> avant la dernière séance.
- Code reproductible (ce repo), README d'installation/exécution.
- Application de démonstration (web).
- Présentation (20 min) : trame disponible dans [`presentation/soutenance.md`](presentation/soutenance.md).

Voir [`project/projets_master.md`](project/projets_master.md) pour les modalités complètes.
