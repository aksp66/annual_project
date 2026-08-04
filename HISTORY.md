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

## 2026-08-04 — Branche personnelle `aaksp`

- Création et push de la branche `aaksp`, espace de travail personnel pour AHLI Kossi Sitsofe Pédro (rôle Model), en dehors de la convention `model/`, `data/`... de `CONTRIBUTING.md`.
- Restriction d'accès en écriture (lui seul) **non appliquée automatiquement** : Git n'a pas de notion d'accès par branche, il faut une règle de protection GitHub (Settings → Branches → Restrict who can push to matching branches) — à configurer manuellement par le propriétaire du repo.

---

## 2026-08-04 — Choix du dataset : Fashion-MNIST

Travail réalisé sur la branche `aaksp` (non mergé sur `master`), première tâche de la Phase 1 (`PLANNING.md`) / checklist "Choix du dataset" (`TASKS.md`).

- Environnement : création du venv (`.venv`), installation de `requirements.txt` (`torch` 2.13 CPU-only, `torchvision` 0.28 — pas de GPU disponible sur la machine de dev).
- Ajout de `scripts/compare_datasets.py` : télécharge Fashion-MNIST et CIFAR-10 via `torchvision.datasets` dans `data/raw/`, vérifie le chargement local (`DataLoader`, shapes, plage de pixels) et affiche un comparatif chiffré.
- Résultats mesurés :

  |Dataset|Train|Test|Taille image|Classes|Poids disque|Temps de chargement|
  |---|---|---|---|---|---|---|
  |Fashion-MNIST|60000|10000|(1, 28, 28)|10|81.85 Mo|33.9 s|
  |CIFAR-10|50000|10000|(3, 32, 32)|10|177.59 Mo|1413.6 s (~23 min)|

  - Ratio de volume de calcul par image (pixels × canaux) CIFAR-10 vs Fashion-MNIST : **x3.92**.
  - Chargement `DataLoader` vérifié pour les deux (shape batch correcte, pixels normalisés dans [0, 1] via `ToTensor`).
  - Licence/disponibilité : les deux sont standard, publics, chargés nativement par `torchvision.datasets` sans restriction pour un usage académique.

- **Décision actée : Fashion-MNIST.**
  - Justification : pas de GPU disponible (CPU only) et budget de calcul du rôle Model limité (~14h pour DDPM + GAN + étude d'ablation, cf. `PLANNING.md`). Fashion-MNIST est ~4x moins coûteux par image (niveaux de gris 28×28 vs RGB 32×32), et son volume/poids sur disque est nettement plus léger et rapide à charger. Le format simple (1 canal, 10 classes équilibrées, `torchvision.datasets.FashionMNIST`) convient bien à une implémentation from scratch d'un U-Net de débruitage et d'un DCGAN dans le temps imparti, tout en restant assez complexe visuellement pour une comparaison DDPM vs GAN pertinente (contrairement à MNIST chiffres, plus trivial).
  - CIFAR-10 downscalé reste documenté comme alternative écartée : complexité RGB inutile au vu du budget de calcul CPU disponible.
- **Prochaine étape :** EDA de Fashion-MNIST (distributions de classes, exemples, statistiques de pixels) dans `notebooks/`.

---

## 2026-08-04 — EDA Fashion-MNIST

Travail réalisé sur la branche `aaksp` (non mergé sur `master`), checklist "EDA (analyse exploratoire)" de `TASKS.md`.

- Ajout de `notebooks/01_eda_dataset.ipynb` (convention de nommage `NN_sujet.ipynb` de `notebooks/README.md`), exécuté de bout en bout (`jupyter nbconvert --execute --inplace`).
- Environnement : installation complète de `requirements.txt` dans le venv (pandas, scikit-learn, matplotlib, jupyter/nbconvert/ipykernel, fastapi, streamlit... manquaient, seuls torch/torchvision avaient été installés lors du choix du dataset).
- Résultats de l'EDA :
  - **Format** : train `(60000, 28, 28)` uint8, test `(10000, 28, 28)` uint8, labels `int64`, 1 canal (niveaux de gris), pixels dans [0, 255].
  - **Valeurs manquantes / corrompues** : 0 NaN, 0 label manquant, correspondance images/labels 1-à-1 vérifiée sur train et test.
  - **Valeurs aberrantes** : dimensions uniques `(28, 28)` sur toutes les images, aucun pixel hors [0, 255].
  - **Doublons exacts** (hash MD5 par image) : 0 doublon en train (60000 images uniques), 0 en test (10000 uniques).
  - **Équilibre des classes** : parfaitement équilibré — 6000 images/classe en train, 1000/classe en test, 10 classes.
  - **Statistiques pixels (train, échelle [0,1])** : moyenne = 0.2860, écart-type = 0.3530 (moyenne = 72.94, écart-type = 90.02 en échelle [0,255]) — base pour la normalisation du `DataLoader`.
  - **Visualisation** : échantillon de 6 images par classe affiché ; classes visuellement proches identifiées (`Shirt` vs `T-shirt/top` vs `Coat` vs `Pullover`), pertinent pour juger la finesse de génération DDPM vs GAN.
- **Observations consignées** (section "Données" du rapport) : dataset propre nativement (pas de nettoyage requis), pas de resize nécessaire (déjà 28×28), normalisation recommandée vers [-1, 1] pour la diffusion (`x_norm = (x/255 - 0.5) / 0.5`).
- Checklist "EDA" de `TASKS.md` cochée.
- **Prochaine étape :** pipeline de chargement/prétraitement (`src/data/`, `configs/data.yaml`) — `Dataset`/`DataLoader` PyTorch, normalisation, split train/éval, test unitaire de shape/plage de valeurs.

---

## 2026-08-04 — Pipeline de chargement / prétraitement

Travail réalisé sur la branche `aaksp` (non mergé sur `master`), checklist "Pipeline de chargement / prétraitement" de `TASKS.md`.

- Ajout de `configs/data.yaml` : dataset `fashion_mnist`, `image_size: 32` (pad 28→32 pour que le U-Net DDPM downsample par divisions entières par 2 : 32→16→8→4), normalisation `mean=0.5, std=0.5` (pixels dans [-1, 1], cf. observations de l'EDA), `val_split: 0.1`, `seed: 42`, `batch_size: 128`.
- Ajout de `src/data/dataset.py` : `load_config()` (lecture YAML), `build_transform()` (pad + normalisation), `get_dataloaders()` — construit train/val/test `DataLoader` ; le split val est prélevé sur le train set officiel (seed fixé via `torch.Generator`), le test set officiel reste réservé à l'évaluation finale (FID).
- Ajout de `src/utils/seed.py` (`set_seed()` — random/numpy/torch/cuda) pour la reproductibilité des futurs entraînements.
- Ajout de `pytest` à `requirements.txt` (absent jusqu'ici, nécessaire pour les tests unitaires prévus dans `tests/`).
- Ajout de `tests/test_data.py` (3 tests, tous passants) :
  - shape de sortie du DataLoader `(128, 1, 32, 32)` et pixels dans [-1, 1] ;
  - tailles des splits train/val/test cohérentes (54000/6000/10000) ;
  - reproductibilité du split train/val avec le seed fixé (mêmes indices entre deux appels).
- Checklist "Pipeline de chargement / prétraitement" de `TASKS.md` cochée.
- **Prochaine étape :** rôle Model — processus de diffusion direct (bruitage) from scratch (`src/models/ddpm/`), première brique du DDPM.

---

## 2026-08-04 — Processus de diffusion direct (forward), from scratch

Travail réalisé sur la branche `aaksp` (non mergé sur `master`), checklist "Processus de diffusion (forward) — from scratch" de `TASKS.md`, rôle Model.

- Ajout de `src/models/ddpm/diffusion.py` :
  - `make_beta_schedule()` : schedule `linear` (Ho et al. 2020) et `cosine` (Nichol & Dhariwal 2021), les deux implémentés et testés.
  - `GaussianDiffusion` : précalcule `betas`, `alphas`, `alphas_cumprod` et leurs racines ; `q_sample(x0, t, noise)` implémente la **formule fermée** `x_t = sqrt(ᾱ_t)·x_0 + sqrt(1-ᾱ_t)·noise`, donc un bruitage direct à un pas `t` arbitraire sans boucle sur les pas intermédiaires.
- Ajout de `configs/ddpm_base.yaml` : baseline `timesteps=1000`, `schedule=linear`, `beta_start=1e-4`, `beta_end=0.02` (valeurs standard Ho et al. 2020). Servira de base à l'étude d'ablation sur le nombre de pas (Phase 2 de `PLANNING.md`).
- Ajout de `tests/test_diffusion.py` (6 tests, tous passants) : shape/bornes du schedule linéaire, schedule cosine fonctionnel, shape de `q_sample`, `x_t ≈ x_0` à `t=0`, bruit croissant avec `t`, et surtout **`x_T` statistiquement proche de `N(0,1)`** (moyenne/écart-type mesurés sur 2000 échantillons, tolérance 0.05).
- Ajout de `notebooks/02_diffusion_forward.ipynb` (exécuté de bout en bout) : vérification visuelle du bruitage progressif sur 4 images Fashion-MNIST à `t ∈ {0, 50, 100, 250, 500, 999}`, histogramme des pixels de `x_T` superposé à la gaussienne théorique. Résultat mesuré : `x_T` moyenne=-0.0038, écart-type=1.0033 — conforme à l'attendu.
- Checklist "Processus de diffusion (forward)" de `TASKS.md` cochée.
- **Prochaine étape :** rôle Model — U-Net de débruitage + processus inverse (`src/models/ddpm/`), embedding du pas de temps, loss MSE, boucle d'échantillonnage.
