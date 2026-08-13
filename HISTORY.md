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
- Ajout d'un tableau "Responsabilités par dossier" dans `CONTRIBUTING.md` : un responsable principal par domaine (Data/Experiment Engineer, Model/Research Engineer, Reporting/Backend Developer), sans restriction d'accès technique (impossible nativement sur GitHub à l'échelle d'un sous-dossier). Un `CODEOWNERS` pourra être ajouté une fois les identifiants GitHub de l'équipe connus.
- Invitations GitHub envoyées et en attente de réponse : `anne952` (KONTEVI Akossiwa Anne), `Mabelle95` (KOYE Leleda Ma Belle) — attribution des rôles à confirmer.
- Précision de la règle de review dans `CONTRIBUTING.md` : le·la responsable d'un dossier ne relit jamais sa propre PR ; à 3, la review revient à l'un·e des deux autres membres.

---

## 2026-08-04 — Planning de travail

- Ajout de `PLANNING.md` : découpage des tâches par phase (Cadrage, Données+Modèle, API+App+Docker, Finalisation — calé sur les 14 séances du cours), par rôle et durée estimée, avec livrable associé à chaque tâche.
- Charge totale indicative par rôle (Data ~5h, Model ~14h, Backend ~9h) à ajuster une fois les rôles nommément attribués et le dataset tranché.
- Lien ajouté depuis `Readme.md`.
- **Reste à faire :** attribution nominative des rôles (toi, `anne952`, `Mabelle95`), choix définitif du dataset (Fashion-MNIST vs CIFAR-10 downscalé).

---

## 2026-08-04 — Détail des tâches par rôle et fonctionnalité

- Ajout de `TASKS.md` : chaque fonctionnalité de `PLANNING.md` (choix du dataset, EDA, pipeline de données, diffusion forward/U-Net, DCGAN, entraînement baseline, étude d'ablation, évaluation, API, app, Docker, rapport, présentation) décomposée en checklist d'actions concrètes par rôle.
- Liens croisés ajoutés entre `Readme.md`, `PLANNING.md` et `TASKS.md`.

---

## 2026-08-04 — Premier rôle attribué

- AHLI Kossi Sitsofe Pédro se positionne comme **Model / Research Engineer** (principal), avec un appui secondaire sur **Reporting / Backend Developer**.
- Tableau Équipe du `Readme.md` mis à jour en conséquence.
- **Reste à faire :** répartir Data / Experiment Engineer et Reporting / Backend Developer (principal) entre `anne952` et `Mabelle95`.

---

## 2026-08-04 — Équipe complète

- **Rôles finalisés :** KOYE Leleda Ma Belle (`Mabelle95`) — Data / Experiment Engineer ; AHLI Kossi Sitsofe Pédro (`aksp66`) — Model / Research Engineer (principal), appui Backend ; KONTEVI Akossiwa Anne (`anne952`) — Reporting / Backend Developer.
- Tableau Équipe du `Readme.md` complété avec les identifiants GitHub.
- Table "Responsabilités par dossier" de `CONTRIBUTING.md` mise à jour avec les noms.
- Ajout de `.github/CODEOWNERS` : demande automatique de review au bon responsable par dossier sur chaque PR, reflète la table de `CONTRIBUTING.md`.

---

## 2026-08-04 — Branche personnelle `aaksp`

- Création et push de la branche `aaksp`, espace de travail personnel pour AHLI Kossi Sitsofe Pédro (rôle Model), en dehors de la convention `model/`, `data/`... de `CONTRIBUTING.md`.
- Restriction d'accès en écriture (lui seul) **non appliquée automatiquement** : Git n'a pas de notion d'accès par branche, il faut une règle de protection GitHub (Settings → Branches → Restrict who can push to matching branches) — à configurer manuellement par le propriétaire du repo.

---

## 2026-08-13 — Choix du dataset : Fashion-MNIST

**Décision (Data / Experiment Engineer) :** Fashion-MNIST retenu comme dataset principal pour le DDPM et le GAN.

- Téléchargement et vérification (checksum torchvision) de Fashion-MNIST (60 000 train / 10 000 test, 28×28, niveaux de gris) et CIFAR-10 (50 000 train / 10 000 test, 32×32, RGB) via `scripts/download_and_eda.py`. Réseau local instable (coupures de connexion récurrentes) : ajout de `scripts/resumable_download.py`, téléchargeur avec reprise HTTP Range + retries, utilisé en secours pour finaliser le téléchargement des deux datasets.
- EDA rapide : les deux datasets sont propres (pas de valeurs manquantes, classes strictement équilibrées à 10 classes), voir `reports/datasets_report.json` et échantillons visuels dans `reports/samples/`.
- **Justification du choix :** budget de calcul du cours limité (~28h au total, ~5h dédiées au rôle Data) et nécessité d'entraîner DDPM + GAN + au moins 3 configurations d'ablation (nombre de pas de diffusion). Fashion-MNIST (niveaux de gris, 28×28, ~30 Mo) permet des temps d'entraînement nettement plus courts que CIFAR-10 (couleur, 32×32, 3 canaux, ~170 Mo), laissant plus de marge pour l'étude d'ablation et les itérations, sans perdre la capacité à observer une différence qualitative significative entre DDPM et GAN.
- **Prochaine étape :** pipeline de chargement/prétraitement (`src/data/`), normalisation dans [-1, 1], config `configs/data.yaml`.
