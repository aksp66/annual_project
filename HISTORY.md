# Historique du projet

Journal chronologique des actions réalisées sur le projet. Une entrée par jour d'activité ; mis à jour à chaque action significative (structure, données, entraînement, résultats, rapport...).

---

## 2026-08-04 — Initialisation du repository

**Sujet retenu :** Projet 3 — *Modèle de diffusion (DDPM) entraîné from scratch vs. GAN* (cours Projets AI & Big Data, TCHAYE-KONDI Jude, Ph.D.).

- Création du repository GitHub `annual_project_M1` (`aksp66/annual_project_M1`) et premier commit (`initialisation des bases du projets`).
- Ajout des documents de cadrage du cours dans `project/` (slides PDF, `projets_master.md` avec les modalités de soumission niveau Master).
- **Invitation des membres de l'équipe à rejoindre le repo** : à faire manuellement via GitHub (Settings → Collaborators) ou en fournissant leurs identifiants GitHub — noms/rôles à confirmer, voir section "Équipe" à compléter dans `Readme.md`.
- Mise en place de la structure du projet :
  - `src/` — code source, découpé en `data/` (chargement/prétraitement), `models/ddpm/` et `models/gan/` (architectures), `training/` (boucles d'entraînement), `evaluation/` (FID, métriques, comparaison), `utils/` (seed, logging).
  - `data/` — `raw/` et `processed/`, non versionnées (voir `.gitignore`).
  - `notebooks/` — exploration et prototypage (EDA à venir).
  - `configs/` — un fichier YAML par configuration d'expérience, base de l'étude d'ablation (nombre de pas de diffusion).
  - `experiments/` — sorties d'entraînement (checkpoints, logs, échantillons), non versionnées.
  - `app/` — démo (`api/` FastAPI, `web/` Streamlit) pour générer et comparer DDPM/GAN côte à côte.
  - `docker/` — conteneurisation, à remplir une fois l'API et l'app développées.
  - `reports/` — source du rapport final (style article scientifique).
  - `scripts/` — scripts de reproduction (téléchargement des données, lancement des entraînements par config).
  - `tests/` — tests unitaires.
  - Chaque dossier de code/données contient un `README.md` expliquant son rôle.
- Ajout de `.gitignore` (données, checkpoints, environnements virtuels) et `requirements.txt` (PyTorch, torchvision, torchmetrics, FastAPI, Streamlit...).
- Réécriture de `Readme.md` : présentation du projet, structure du repo, instructions d'installation.

**Prochaine étape :** exploration des datasets candidats (Fashion-MNIST vs CIFAR-10 downscalé) pour trancher selon le volume, la complexité visuelle et le budget de calcul disponible.

---

## 2026-08-04 — Convention de branches

- Ajout de `CONTRIBUTING.md` : stratégie de branches (GitHub Flow simplifié, `master` protégé, branches courtes préfixées `data/`, `model/`, `exp/`, `app/`, `docker/`, `docs/`), workflow de Pull Request, rappel des exigences de reproductibilité (seed + config + script).
- Lien ajouté depuis `Readme.md`.
