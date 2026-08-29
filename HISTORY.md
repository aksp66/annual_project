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

---

## 2026-08-04 — U-Net de débruitage + processus inverse

Travail réalisé sur la branche `aaksp` (non mergé sur `master`), checklist "U-Net de débruitage + processus inverse" de `TASKS.md`, rôle Model.

- Ajout de `src/models/ddpm/unet.py` :
  - `SinusoidalTimeEmbedding` (embedding du pas `t`, façon Transformer), suivi d'un petit MLP (`Linear → SiLU → Linear`).
  - `ResidualBlock` : GroupNorm + SiLU + conv, injection de l'embedding temporel, connexion résiduelle (projection 1×1 si les canaux changent).
  - `UNet` : downsampling/upsampling avec skip connections, résolutions `32 → 16 → 8` (`channel_mults=[1,2,4]`, `base_channels=32`, 2 blocs résiduels par niveau). **Pas d'attention** — choix délibéré pour rester entraînable sur CPU (pas de GPU disponible, cf. décision dataset). ~3.54M paramètres.
- Extension de `src/models/ddpm/diffusion.py` (`GaussianDiffusion`) :
  - `p_losses(model, x0, t)` : loss MSE entre bruit réel et bruit prédit par le U-Net.
  - `p_sample(model, x_t, t)` : un pas du processus inverse (sampling ancestral), variance a posteriori `posterior_variance` précalculée (Ho et al. 2020, eq. 7).
  - `p_sample_loop(model, shape)` : boucle complète `x_T` (bruit pur) → `x_0`.
- Mise à jour de `configs/ddpm_base.yaml` : section `model` (`in_channels`, `base_channels`, `channel_mults`, `num_res_blocks`).
- Ajout de `src/utils/viz.py` (`save_sample_grid`) : sauvegarde une grille d'échantillons générés (dénormalisation [-1,1]→[0,1]), destinée à être appelée à intervalles réguliers pendant l'entraînement baseline.
- Ajout de `tests/test_unet.py` (5 tests, tous passants) : shape de sortie du U-Net = shape d'entrée (plusieurs batch sizes/`t`), loss scalaire et finie, shape de `p_sample`, `p_sample_loop` de bout en bout sans NaN.
- Ajout de `notebooks/03_unet_smoke_test.ipynb` (exécuté de bout en bout, ~36 min) — vérification mécanique avant l'entraînement baseline complet (pas un entraînement réel) :
  - Shapes vérifiées sur un batch réel (128, 1, 32, 32).
  - 300 pas de gradient (Adam, lr=2e-4) : **loss MSE 1.044 → 0.050**, confirme que le gradient circule correctement dans le U-Net et que la loss est apprenable.
  - Boucle de sampling complète (1000 pas) exécutée en 146s, shape de sortie correcte, aucun NaN. Images générées peu réalistes (attendu — 300 pas seulement, pas la baseline).
  - `save_sample_grid` testé, échantillons sauvegardés dans `experiments/ddpm_smoke_test/samples/` (non versionné, cf. `.gitignore`).
- Checklist "U-Net de débruitage + processus inverse" de `TASKS.md` cochée.
- **Prochaine étape :** rôle Model — entraînement DDPM baseline (config par défaut, `experiments/ddpm_baseline/`), puis DCGAN (`src/models/gan/`).

---

## 2026-08-04 — Entraînement DDPM baseline (lancé) + DCGAN

Travail réalisé sur la branche `aaksp` (non mergé sur `master`), rôle Model.

**Entraînement DDPM baseline (`PLANNING.md` Phase 2) :**
- Calibration mesurée hors notebook : **~6.76 s/step** (batch=128, U-Net ~3.54M paramètres, CPU). Sur cette base, `configs/ddpm_base.yaml` complété avec une section `training` (`num_steps: 1000`, `lr: 2e-4`, `sample_every`/`checkpoint_every: 250`) calée sur le budget de 2h de `PLANNING.md` (~1000 steps + 4 cycles de sampling complet ≈ 2h).
- Ajout de `src/training/train_ddpm.py` : script reproductible (`python -m src.training.train_ddpm --config configs/ddpm_base.yaml`), seed fixé, logs CSV (`experiments/ddpm_baseline/log.csv`), checkpoints (`experiments/ddpm_baseline/checkpoints/`) et grilles d'échantillons (`experiments/ddpm_baseline/samples/`) sauvegardés à intervalles réguliers.
- **Entraînement lancé en arrière-plan** (~2h estimées) ; résultats (courbe de loss finale, échantillons) à consigner dans une prochaine entrée `HISTORY.md` une fois terminé.

**DCGAN (`TASKS.md` — rôle Model) :**
- Ajout de `src/models/gan/generator.py` (`Generator`) : 4 blocs `ConvTranspose2d + BatchNorm + ReLU`, `z (100,1,1) → image 32×32×1`, sortie `Tanh` (cohérent avec la normalisation [-1,1] du pipeline de données).
- Ajout de `src/models/gan/discriminator.py` (`Discriminator`) : 4 blocs `Conv2d + LeakyReLU(0.2)` (pas de BatchNorm sur la première couche, cf. Radford et al. 2015), sortie logit brut (compatible `BCEWithLogitsLoss`).
- Ajout de `configs/gan_base.yaml` : `latent_dim=100`, `base_channels=64`, Adam `lr=2e-4, β1=0.5, β2=0.999` (valeurs standard DCGAN), **`num_steps=1000`** — même nombre de steps que le DDPM baseline pour un budget de calcul comparable (cf. `PLANNING.md`).
- Ajout de `src/training/train_gan.py` : boucle d'entraînement alternée D puis G, init des poids `N(0, 0.02)` (Radford et al. 2015), logs CSV incluant **`loss_d`, `loss_g`, `D(real)`, `D(fake)`** à chaque `log_every` — mécanisme de suivi des courbes G/D pour repérer un éventuel mode collapse (ex. `D(fake)` qui stagne près de 0 ou 1, `loss_g` qui explose). L'analyse des courbes elles-mêmes se fera après l'entraînement baseline (prochaine tâche).
- Ajout de `tests/test_gan.py` (5 tests, tous passants) : shape/plage du générateur (`Tanh` → [-1,1]), shape du discriminateur, pipeline G→D bout en bout, backward BCE fonctionnel, betas Adam lus depuis la config.
- Checklists "DCGAN" de `TASKS.md` cochée.
- **Prochaine étape :** attendre la fin de l'entraînement DDPM baseline (résultats à documenter), puis lancer l'entraînement GAN baseline avec le même budget.

---

## 2026-08-04 — Résultats de l'entraînement DDPM baseline

Travail réalisé sur la branche `aaksp` (non mergé sur `master`), rôle Model. Suite de l'entrée précédente : l'entraînement lancé en arrière-plan (`src/training/train_ddpm.py`, `configs/ddpm_base.yaml`) est allé à son terme.

- **Durée réelle** : 7235.6 s (~2h00), 1000 steps, batch=128, CPU uniquement — conforme à l'estimation.
- **Loss MSE** : 1.044 (step 1) → **0.041 en moyenne sur les 20 derniers logs** (min ponctuel 0.027), décroissance stable sans divergence ni plateau anormal.
- **Échantillons générés** (`experiments/ddpm_baseline/samples/`, non versionnés) : progression visuelle nette —
  - `step_000250.png` : formes vagues, à peine des silhouettes.
  - `step_000750.png` : vêtements déjà reconnaissables (silhouette de haut/t-shirt).
  - `step_001000.png` : plusieurs échantillons clairement identifiables comme des vêtements (pantalon, haut), cohérent avec les classes Fashion-MNIST — résultat correct pour seulement 1000 steps sur CPU.
- 4 checkpoints sauvegardés (`experiments/ddpm_baseline/checkpoints/ddpm_step0000{250,500,750,1000}.pt`), logs complets dans `experiments/ddpm_baseline/log.csv`.
- **Limite à noter pour le rapport (section Discussion/Limites)** : budget CPU très inférieur à un entraînement DDPM typique (dizaines de milliers de steps sur GPU) ; les résultats sont corrects mais pas encore optimaux (pas de plateau de convergence atteint, la loss continuait de descendre légèrement en fin d'entraînement).
- **Prochaine étape :** lancer l'entraînement GAN baseline (`configs/gan_base.yaml`, même `num_steps=1000`) pour une comparaison à budget de calcul comparable.

---

## 2026-08-04 — Résultats de l'entraînement GAN baseline + comparaison de stabilité

Travail réalisé sur la branche `aaksp` (non mergé sur `master`), rôle Model. `src/training/train_gan.py` exécuté avec `configs/gan_base.yaml` (même `num_steps=1000` que le DDPM, pour un budget comparable).

- **Durée réelle** : 1012.5 s (~17 min) — **~7x plus rapide que le DDPM** (7235.6 s) pour le même nombre de steps : le GAN ne fait qu'une passe générateur (pas de boucle de débruitage à 1000 pas pour échantillonner), donc à budget de calcul égal en nombre de steps, le coût réel diffère fortement entre les deux familles de modèles — point à chiffrer dans la section "Résultats" du rapport (temps de génération DDPM multi-pas vs GAN one-shot).
- **Loss et scores du discriminateur** (`experiments/gan_baseline/log.csv`) :
  - `loss_d` : 1.757 (step 1) → 0.624 (moy. 20 derniers logs).
  - `loss_g` : 1.562 → 2.251 (moy. 20 derniers), avec des pics ponctuels jusqu'à **5.38** (step 40).
  - `D(real)` : 0.296 → 0.780 ; `D(fake)` : 0.326 → 0.237 — le discriminateur prend l'avantage sur le générateur en fin d'entraînement (déséquilibre net par rapport à l'équilibre théorique à 0.5), instabilité typique d'un GAN mais **pas de mode collapse total** observé (diversité de formes conservée visuellement).
- **Échantillons générés** (`experiments/gan_baseline/samples/`, non versionnés) : `step_000250.png` encore proche de bruit texturé, `step_000750.png`/`step_001000.png` montrent des silhouettes de vêtements (pantalons, hauts) avec des **artefacts en damier** caractéristiques des couches `ConvTranspose2d` (cf. Odena et al., *Deconvolution and Checkerboard Artifacts*, 2016 — à citer en Travaux liés/Discussion).
- Ajout de `notebooks/04_baseline_training_curves.ipynb` (exécuté de bout en bout) : courbes de loss DDPM et GAN (CSV + matplotlib), comparaison `D(real)` vs `D(fake)` par rapport à l'équilibre théorique 0.5. Confirme visuellement : DDPM = décroissance lisse et monotone ; GAN = dynamique adversariale oscillante.
- **Conclusion stabilité (base de la section Discussion du rapport)** : à budget de steps identique, le DDPM converge de façon prévisible et reproductible tandis que le GAN nécessite un suivi actif de l'équilibre G/D et reste plus sensible à l'instabilité — cohérent avec la littérature (Ho et al. 2020 vs Goodfellow et al. 2014).
- Checklist "Entraînement baseline (DDPM + GAN)" de `TASKS.md` cochée (seed/config/budget comparable, deux entraînements lancés, checkpoints réguliers, courbes de loss CSV + matplotlib).
- **Prochaine étape :** étude d'ablation sur le nombre de pas de diffusion (≥3 configs, ex. 100/400/1000).

---

## 2026-08-04 — Étude d'ablation : nombre de pas de diffusion (lancée)

Travail réalisé sur la branche `aaksp` (non mergé sur `master`), rôle Model, checklist "Étude d'ablation (nombre de pas de diffusion)" de `TASKS.md`.

- Extension de `src/training/train_ddpm.py` : à la fin de l'entraînement, mesure isolée du **temps de génération** (`p_sample_loop` chronométré séparément des échantillons périodiques) et écriture d'un `summary.json` par run (`timesteps`, `num_train_steps`, `total_train_time_s`, `final_loss_avg_last20`, `generation_time_s`) — base directe du tableau comparatif de l'ablation.
- Ajout de 3 configs, seule `timesteps` varie (architecture, seed=42, `beta_start`/`beta_end`, budget d'entraînement **identiques** pour une comparaison équitable) :
  - `configs/ddpm_ablation_steps100.yaml` (`timesteps: 100`)
  - `configs/ddpm_ablation_steps400.yaml` (`timesteps: 400`)
  - `configs/ddpm_ablation_steps1000.yaml` (`timesteps: 1000`, distinct de `configs/ddpm_base.yaml` qui reste la config baseline à 1000 steps d'entraînement).
  - Budget d'entraînement réduit à `num_steps: 500` (vs 1000 pour la baseline) pour que les 3 runs d'ablation tiennent dans un temps de calcul CPU raisonnable (~3h estimées pour les 3 runs cumulés).
- **Les 3 entraînements sont lancés séquentiellement en arrière-plan** ; résultats (temps d'entraînement/génération par config, qualité visuelle comparée) à consigner dans une prochaine entrée une fois terminés.
- Checklist `TASKS.md` : "définir les configs" et "lancer chaque config" cochées ; mesure/comparaison/tableau en attente des résultats.

---

## 2026-08-04 — Résultats de l'étude d'ablation (nombre de pas de diffusion)

Travail réalisé sur la branche `aaksp` (non mergé sur `master`), rôle Model. Suite de l'entrée précédente.

**Incident** : le run `T=100` s'est terminé normalement, mais l'exécution en arrière-plan des runs `T=400`/`T=1000` a été interrompue en cours de route (redémarrage de l'environnement de session, pas une erreur du code — `T=400` s'était arrêté au step 50/500 sans checkpoint sauvegardé). Les deux runs manquants ont été relancés depuis le début sans perte pour `T=100` (déjà complet et sauvegardé).

**Résultats finaux** (`summary.json` par config, budget d'entraînement identique = 500 steps) :

|T (pas de diffusion)|Temps entraînement|Temps génération (8 img)|Loss finale (moy. 20 derniers)|
|---|---|---|---|
|100|3295.7 s|13.4 s|0.1107|
|400|3667.6 s|52.0 s|0.0648|
|1000|3798.8 s|129.0 s|0.0404|

- Ajout de `notebooks/05_ablation_diffusion_steps.ipynb` (exécuté de bout en bout) : tableau comparatif, courbes de loss superposées, comparaison visuelle des échantillons finaux (`step_000500.png` des 3 configs), graphiques temps de génération / loss finale vs `T`.
- **Temps de génération** : quasi linéaire en `T` (ratio mesuré ≈ 1 / 3.9 / 9.6, proche du ratio théorique 1/4/10) — confirme le compromis attendu qualité vs coût de génération du DDPM multi-pas.
- **Loss finale** : décroît avec `T` (0.111 → 0.065 → 0.040) — attendu mécaniquement (pas de bruit plus petits à `T` élevé), **pas directement une mesure de qualité perceptuelle**.
- **Qualité visuelle** (résultat le plus intéressant, contre-intuitif) : à budget d'entraînement égal (500 steps), **`T=400` produit les échantillons les plus nets** (silhouettes de vêtements reconnaissables) ; `T=100` reste bruité (pas assez de pas pour affiner) ; **`T=1000` est visuellement moins net que `T=400`** malgré sa loss plus basse — avec 500 steps de gradient répartis sur 1000 valeurs de `t` possibles, chaque `t` est en moyenne moins souvent vu qu'avec `T` plus petit, donc le modèle est comparativement sous-entraîné à `T` élevé. Cohérent avec le run baseline (`configs/ddpm_base.yaml`, `T=1000` mais **1000** steps d'entraînement) qui produisait des échantillons nettement plus nets — **le nombre de steps d'entraînement nécessaire semble croître avec `T`**, point à developper en Discussion du rapport.
- **Conclusion pour le rapport** : sur ce budget de calcul CPU contraint, `T=400` offre le meilleur compromis qualité/coût de génération parmi les 3 valeurs testées ; `T=1000` (choix standard Ho et al. 2020, utilisé pour la baseline) reste préférable seulement si le budget d'entraînement est suffisant pour l'exploiter pleinement.
- Checklist "Étude d'ablation (nombre de pas de diffusion)" de `TASKS.md` cochée intégralement.
- **Prochaine étape :** rôle Model — métriques (FID ou évaluation qualitative structurée) et comparaison finale chiffrée DDPM vs GAN.

---

## 2026-08-04 — Comparaison chiffrée DDPM vs GAN (FID, diversité, temps de génération)

Travail réalisé sur la branche `aaksp` (non mergé sur `master`), rôle Model, checklist "Évaluation et comparaison DDPM vs GAN" de `TASKS.md`.

- Ajout de `src/evaluation/metrics.py` : `compute_fid()` (FID via `torchmetrics.image.fid.FrechetInceptionDistance`, feature=2048/InceptionV3, conversion [-1,1]/1 canal → [0,1]/3 canaux), `pixel_variance()` (variance intra-batch, proxy de diversité) et `count_near_duplicate_pairs()` (détection de quasi-doublons par distance euclidienne normalisée). Ajout de `torch-fidelity` à `requirements.txt` (dépendance requise par `FrechetInceptionDistance`, poids InceptionV3 ~91 Mo téléchargés une fois).
- Ajout de `tests/test_metrics.py` (6 tests, tous passants) : shape/plage de `to_fid_input`, variance nulle/positive selon les images, détection correcte des doublons stricts, FID positif et fini sur deux tirages de la même distribution.
- Ajout de `notebooks/06_evaluation_ddpm_vs_gan.ipynb` (exécuté de bout en bout, ~31 min) : charge les checkpoints baseline (`ddpm_step001000.pt`, `gan_step001000.pt`), génère 100 images par modèle (taille du jeu limitée par le budget CPU), calcule FID vs 100 images réelles du test set, diversité, temps de génération.

**Résultats mesurés (protocole identique, 100 images/groupe) :**

|Métrique|DDPM|GAN|
|---|---|---|
|Temps de génération (100 img)|1854.0 s (18.54 s/image)|0.09 s (0.0009 s/image)|
|**Ratio temps de génération**|DDPM ~21600x plus lent que le GAN (génération one-shot vs 1000 pas séquentiels)||
|FID (vs réel)|**114.12**|173.47|
|Variance intra-batch|0.2443|0.2292 (réel : 0.2840)|
|Quasi-doublons (100 img, seuil 0.05)|0|0|

- **FID** : le DDPM baseline obtient un score nettement meilleur (114 vs 173) que le GAN baseline sur ce protocole — cohérent avec l'observation qualitative des runs précédents (échantillons DDPM plus nets à step 1000, GAN affecté par des artefacts en damier). **À nuancer** : calculé sur seulement 100 images/groupe (la littérature recommande plusieurs milliers pour un FID stable) — valable comme comparaison relative DDPM vs GAN sur un protocole identique, pas comme score absolu comparable à la littérature.
- **Diversité** : aucun quasi-doublon détecté pour les deux modèles ; variance intra-batch légèrement inférieure à celle des images réelles pour les deux (attendu, léger mode-seeking), le DDPM restant plus proche de la variance réelle que le GAN — pas de mode collapse sévère confirmé pour le GAN, cohérent avec l'entraînement baseline.
- **Temps de génération** : confirme structurellement le compromis DDPM (multi-pas, coûteux) vs GAN (one-shot, quasi instantané) — à mettre en regard de l'étude d'ablation (`T` plus faible réduit fortement ce coût, cf. entrée précédente).
- **Limite non traitée** (à noter en Discussion/Limites du rapport) : la comparaison de stabilité GAN vs DDPM sur **plusieurs seeds** n'a pas été réalisée (budget CPU déjà très sollicité sur cette session — chaque run baseline supplémentaire coûterait ~1-2h) ; la conclusion de stabilité repose ici sur un seul seed (42) par modèle, cf. entrées précédentes (courbes de loss G/D, D(real)/D(fake)).
- Checklist `TASKS.md` : FID, diversité et temps de génération cochés ; stabilité multi-seeds laissée non cochée (limite documentée ci-dessus).
- **Prochaine étape :** rédaction continue du rapport (sections Données + Méthode, rôle Backend) et comparaison finale chiffrée pour la Phase 4.

---

## 2026-08-04 — Scripts de reproductibilité (rôle Data)

Travail réalisé sur la branche `aaksp` (non mergé sur `master`), checklist "Scripts de reproductibilité" de `TASKS.md` (rôle Data, mais complétée pour clore les fondations avant la suite du planning).

- Ajout de `scripts/prepare_data.py` : télécharge/prépare Fashion-MNIST à partir d'une config (`configs/data.yaml`), affiche tailles des splits et vérifie shape/plage de valeurs d'un batch — automatise ce qui était fait manuellement dans `scripts/compare_datasets.py`.
- Ajout de `scripts/train.py --config <path>` : point d'entrée générique qui détecte automatiquement le type de config (`timesteps` → DDPM, `model.latent_dim` → GAN) et délègue à `src.training.train_ddpm`/`train_gan` — satisfait la convention `scripts/train.py --config ...` de `TASKS.md`, en plus des invocations directes déjà utilisées (`python -m src.training.train_ddpm ...`).
- Ajout de `tests/test_reproducibility.py` : lance deux entraînements DDPM identiques (config minuscule dédiée au test — `timesteps=5`, petit U-Net, 3 steps — pour rester rapide) avec le même seed, et vérifie que la séquence de loss produite est strictement identique entre les deux runs. **Confirme la reproductibilité du pipeline** (seed fixé via `set_seed`, chargement de données déterministe, pas de source d'aléa non contrôlée).
- Suite de tests complète : 26 tests passants (5 nouveaux fichiers de tests cumulés depuis le début : data, diffusion, gan, metrics, reproducibility, unet).
- Checklist "Scripts de reproductibilité" de `TASKS.md` cochée intégralement — clôture les fondations Data/Model de la Phase 2.
- **Prochaine étape :** rédaction du rapport (`reports/`, rôle Backend) ou démarrage de la Phase 3 (API/App/Docker), selon priorité.

---

## 2026-08-04 — API FastAPI (Phase 3, appui Backend)

Travail réalisé sur la branche `aaksp` (non mergé sur `master`), checklist "API (FastAPI)" de `TASKS.md`, en appui du rôle Backend (cf. positionnement de rôle du 2026-08-04).

- Ajout de `app/api/main.py` : charge les checkpoints DDPM (`experiments/ddpm_baseline/checkpoints/ddpm_step001000.pt`) et GAN (`experiments/gan_baseline/checkpoints/gan_step001000.pt`) une fois au démarrage (`lifespan` FastAPI), avec repli silencieux si un checkpoint est absent (`models` ne contient alors pas la clé correspondante).
  - `GET /health` : statut + liste des modèles effectivement chargés.
  - `GET /generate?model=ddpm|gan&n=...` : génère `n` images, retourne un JSON `{model, n, images: [base64 PNG, ...]}`. Validation du paramètre `model` via `Literal["ddpm","gan"]` (→ 422 automatique si invalide) ; `n` plafonné (`MAX_N_DDPM=4`, `MAX_N_GAN=16` — la génération DDPM coûte ~18s/image en CPU, cf. entrée d'évaluation précédente) → 400 si dépassé ; 503 si le modèle demandé n'est pas chargé.
- Ajout de `tests/test_api.py` (6 tests, tous passants, `fastapi.testclient.TestClient`) : `/health`, génération GAN (PNG valide décodé), paramètre `model` invalide → 422, `n` trop grand → 400 (DDPM et GAN), génération DDPM réelle (1 image, ~18s, confirme le chemin complet checkpoint → sampling → PNG).
- Test manuel du serveur réel (`uvicorn app.api.main:app`) : `/generate?model=gan` et validation d'erreur confirmés en conditions réelles (logs uvicorn).
- Ajout de `httpx` à `requirements.txt` (requis par `TestClient`).
- Checklist "API (FastAPI)" de `TASKS.md` cochée intégralement.
- **Prochaine étape :** application Streamlit (`app/web/`) consommant cette API, puis Docker.

---

## 2026-08-04 — Application Streamlit (Phase 3, appui Backend)

Travail réalisé sur la branche `aaksp` (non mergé sur `master`), checklist "Application web (Streamlit)" de `TASKS.md`.

- Ajout de `app/web/app.py` : sélecteur de modèle (`DDPM` / `GAN` / `Comparaison côte à côte`), slider du nombre d'images (plafonné par modèle, cohérent avec les limites de l'API), bouton "Générer" appelant `GET /generate` de l'API (`requests`), affichage des images décodées (base64 → PNG), et un bloc de métriques indicatives par génération : FID de référence (114.12 DDPM / 173.47 GAN, mesurés dans `notebooks/06_evaluation_ddpm_vs_gan.ipynb`) + temps de génération mesuré en direct sur la requête en cours.
- `API_URL` configurable par variable d'environnement (`http://localhost:8000` par défaut) — préparation pour Docker (services séparés `api`/`web`).
- Ajout de `requests` à `requirements.txt`.
- **Test réalisé** : API (`uvicorn`) et app (`streamlit run --server.headless true`) lancées ensemble ; la page se charge sans exception (HTTP 200, logs Streamlit propres). **Limite** : pas d'outil de navigation/clic automatisé disponible dans cet environnement pour simuler un clic sur "Générer" en conditions réelles — le contrat d'API sous-jacent (`GET /generate`) est déjà couvert par les 6 tests automatisés de `tests/test_api.py` et par un test manuel `curl` réussi (entrée précédente), donc le risque résiduel est faible mais non nul (ex. rendu Streamlit lui-même).
- Checklist "Application web (Streamlit)" de `TASKS.md` cochée intégralement (avec la réserve de test ci-dessus).
- **Prochaine étape :** Docker (Dockerfiles api/app + `docker-compose.yml`).

---

## 2026-08-05 — Conteneurisation (Docker), fin de la Phase 3

Travail réalisé sur la branche `aaksp` (non mergé sur `master`), checklist "Docker" de `TASKS.md`.

- Ajout de `docker/api.Dockerfile` et `docker/web.Dockerfile` (`python:3.11-slim`, choix délibéré plutôt que la version 3.14 de la machine de dev — meilleure disponibilité des wheels pour tout `requirements.txt`, cf. décision dataset/venv). `PYTHONPATH=/app` sur l'image API pour que `from src... import ...` résolve correctement dans le conteneur.
- Ajout de `docker-compose.yml` (racine du repo) : services `api` (port 8000) et `web` (port 8501, `API_URL=http://api:8000` pour la résolution DNS interne Docker Compose), `web` dépend de `api`.
- **Checkpoints entraînés montés en volume** (`./experiments:/app/experiments:ro`) plutôt que copiés dans l'image : ils ne sont pas versionnés (cf. `.gitignore`), trop volumineux, et un montage évite de reconstruire l'image à chaque nouvel entraînement.
- Ajout de `.dockerignore` (`.venv/`, `data/`, `experiments/`, `notebooks/`, etc.) pour accélérer l'envoi du contexte de build.
- **Test de bout en bout réalisé** (`docker compose build` puis `docker compose up -d`) : images construites (9.23 Go chacune, disque ; 3.12 Go de contenu — `requirements.txt` complet non allégé pour Docker, simplification assumée vu l'exigence allégée niveau Master, cf. `app/README.md`) ; `GET /health` du conteneur `api` confirme les 2 modèles chargés (checkpoints lus depuis le volume) ; `GET /generate?model=gan&n=1` renvoie un PNG valide depuis le conteneur ; page Streamlit du conteneur `web` répond HTTP 200 ; **connectivité réseau interne `web` → `api` vérifiée** (`docker exec` dans le conteneur `web`, requête vers `http://api:8000/health` réussie) — confirme que la résolution DNS Docker Compose fonctionne, donc que le bouton "Générer" de l'app fonctionnera en conditions réelles. Conteneurs arrêtés/supprimés après test (`docker compose down`).
- `Readme.md` mis à jour : section "Démo (API + app)" avec commande `docker compose up --build`, tableau ports/variables d'environnement, note sur la nécessité d'avoir entraîné les baselines localement au préalable (503 sinon), alternative sans Docker.
- Checklist "Docker" de `TASKS.md` cochée intégralement — **clôture la Phase 3** (API + App + Docker) de `PLANNING.md`.
- **Prochaine étape :** rédaction du rapport (`reports/`) et/ou Phase 4 (comparaison finale, relecture, reproductibilité `docker compose up --build`).

---

## 2026-08-06 — Premier jet du rapport (reports/rapport.docx)

Travail réalisé sur la branche `aaksp` (non mergé sur `master`), checklist "Rapport (style article scientifique)" de `TASKS.md`.

- Contraintes de mise en forme demandées : noir et blanc uniquement (aucune autre couleur), police Tahoma, taille normale 12, avec sommaire, table des matières et glossaire.
- Ajout de `reports/generate_report.py` : génère `reports/rapport.docx` par script (`python-docx`), pour que le rapport reste reproductible/régénérable comme le reste du projet plutôt que rédigé à la main dans Word.
  - Styles `Normal`/`Heading 1-3`/`Title` forcés en Tahoma, noir (`RGBColor(0,0,0)`), tailles 12/16/14/12/22pt (titre) — aucune couleur de thème Word par défaut.
  - Style `Hyperlink` **déclaré explicitement** en noir sans soulignement : sans cela, Word aurait recréé ce style avec son bleu souligné par défaut dès la mise à jour du champ TOC, violant la contrainte N&B — bug détecté et corrigé pendant la génération (vérifié par relecture programmatique du docx après coup).
  - Champ TOC Word natif (`add_toc_field`, niveaux 1-3) + `w:updateFields` activé dans `settings.xml` pour que la table des matières se peuple automatiquement à l'ouverture dans Word (à défaut, mise à jour manuelle clic droit).
  - "Sommaire" (liste simple des sections) distinct de la "Table des matières" (champ Word détaillé, avec numéros de page), conformément à la demande.
  - "Glossaire" : 18 termes définis (DDPM, GAN, DCGAN, U-Net, FID, timestep, seed, checkpoint, mode collapse, Docker/volume, etc.).
- Figures extraites des notebooks et converties en niveaux de gris (`reports/figures/`, 8 images) pour respecter la contrainte N&B même sur les graphiques matplotlib (barres bleu/orange par défaut) : distribution des classes, échantillons Fashion-MNIST, bruitage progressif, échantillons DDPM/GAN baseline, comparaison ablation (temps/loss vs T, échantillons), comparaison réel/DDPM/GAN.
- Contenu rédigé pour toutes les sections imposées (Introduction, Travaux liés, Données, Méthode, Étude d'ablation, Résultats, Déploiement, Discussion et limites, Répartition du travail, Références), à partir des chiffres et décisions déjà journalisés dans les entrées précédentes de ce fichier — 6 tableaux numérotés, 8 figures numérotées.
- **Section "Répartition du travail" rédigée honnêtement** : à ce stade, l'ensemble du travail (Data, Model, Backend API/App/Docker) a été réalisé par AHLI Kossi Sitsofe Pédro sur `aaksp`, faute de contributions encore intégrées de `Mabelle95`/`anne952` — signalé explicitement plutôt que masqué, à corriger une fois leurs apports intégrés.
- Vérification programmatique post-génération (relecture du XML du `.docx`) : police/taille/couleur correctes sur le style `Normal`, les titres, les cellules de tableaux, et le style `Hyperlink` ; champ TOC et `updateFields` présents. Pas d'outil de rendu PDF/Word disponible dans cet environnement pour une vérification visuelle complète (LibreOffice absent) — **à relire visuellement dans Word avant envoi final**.
- Checklist "Rapport" de `TASKS.md` : toutes les sections de contenu cochées ; "Répartition du travail" et "Mise en page finale" laissées en attente (nécessitent les apports des autres membres et une relecture finale).
- **Prochaine étape :** relecture visuelle dans Word, intégration des contributions Data/Backend des autres membres, puis présentation (slides + démo).

---

## 2026-08-06 — Vérification et correction des README de sous-dossiers

Travail réalisé sur la branche `aaksp` (non mergé sur `master`). Comparaison systématique des 9 `README.md` de sous-dossiers (hors `.pytest_cache/README.md`, généré par pytest) au contenu réel de leur dossier.

- **Inexactitudes corrigées :**
  - `docker/README.md` : indiquait encore "à remplir une fois l'API et l'application développées" — corrigé pour refléter que Dockerfiles + `docker-compose.yml` sont faits et testés (renvoi vers l'entrée du 2026-08-05).
  - `scripts/README.md` : annonçait que `scripts/` contenait le "calcul du FID" — en réalité dans `src/evaluation/metrics.py`, utilisé depuis un notebook. README corrigé pour lister précisément les 3 scripts réels (`prepare_data.py`, `train.py`, `compare_datasets.py`) et clarifier où se trouve le FID.
  - `data/README.md` : décrivait `processed/` comme contenant des données prétraitées prêtes à l'entraînement — en réalité ce dossier reste vide, le pipeline normalise à la volée dans le `DataLoader` sans rien écrire sur disque. Corrigé pour le dire explicitement.
  - `configs/README.md` : exemple de commande référençant `configs/ddpm_steps100.yaml`, fichier inexistant (le vrai nom est `ddpm_ablation_steps100.yaml`). Corrigé avec les vrais noms de fichiers et `scripts/train.py`.
  - `src/README.md` : mentionnait "Fashion-MNIST / CIFAR-10" pour `src/data/`, alors que le pipeline réel (`dataset.py`) ne charge que Fashion-MNIST (CIFAR-10 n'a servi qu'au script ponctuel de comparaison). Corrigé.
- **Détails mineurs corrigés :** `notebooks/README.md` (exemple `02_diffusion_prototype.ipynb` → `02_diffusion_forward.ipynb`, ajout d'un exemple d'ablation) ; `tests/README.md` (ne listait que 3 des 7 fichiers de test existants — complété avec les 7).
- **Vérifiés corrects, non modifiés :** `app/README.md`, `reports/README.md`.
- **Prochaine étape :** relecture visuelle du rapport dans Word, intégration des contributions des autres membres, présentation.

---

## 2026-08-06 — Revue de code : PR #1 de Mabelle (`data/eda-fashion-mnist`)

- KOYE Leleda Ma Belle (`Mabelle95`) a ouvert la PR #1 « Data/eda fashion mnist » (choix du dataset, EDA, scripts de téléchargement). Revue effectuée par AHLI Kossi Sitsofe Pédro (conforme à `CONTRIBUTING.md` : le·la responsable du dossier `data/` ne relit jamais sa propre PR).
- **Détail des points à corriger consigné dans `HISTORY.md` de la branche `data/eda-fashion-mnist`** (plusieurs points bloquants identifiés : robustesse du téléchargement, contrôles EDA vides de sens sur les données `uint8`, notebook non fonctionnel sur des données image).
- **Statut : PR non mergée**, en attente de correction par Mabelle puis validation par un·e autre membre de l'équipe avant merge sur `master`.

---

## 2026-08-13 — Choix du dataset : Fashion-MNIST

**Décision (Data / Experiment Engineer) :** Fashion-MNIST retenu comme dataset principal pour le DDPM et le GAN.

- Téléchargement et vérification (checksum torchvision) de Fashion-MNIST (60 000 train / 10 000 test, 28×28, niveaux de gris) et CIFAR-10 (50 000 train / 10 000 test, 32×32, RGB) via `scripts/download_and_eda.py`. Réseau local instable (coupures de connexion récurrentes) : ajout de `scripts/resumable_download.py`, téléchargeur avec reprise HTTP Range + retries, utilisé en secours pour finaliser le téléchargement des deux datasets.
- EDA rapide : les deux datasets sont propres (pas de valeurs manquantes, classes strictement équilibrées à 10 classes), voir `reports/datasets_report.json` et échantillons visuels dans `reports/samples/`.
- **Justification du choix :** budget de calcul du cours limité (~28h au total, ~5h dédiées au rôle Data) et nécessité d'entraîner DDPM + GAN + au moins 3 configurations d'ablation (nombre de pas de diffusion). Fashion-MNIST (niveaux de gris, 28×28, ~30 Mo) implique environ 3,5× moins de pixels par image que CIFAR-10 (couleur, 32×32, 3 canaux, ~170 Mo) — estimation par volume de données, **pas un temps d'entraînement mesuré** sur le matériel du projet. Ce choix laisse plus de marge pour l'étude d'ablation et les itérations, sans perdre la capacité à observer une différence qualitative significative entre DDPM et GAN. Un vrai chronométrage sera fait à l'entraînement baseline (Phase 2).
- **Prochaine étape :** pipeline de chargement/prétraitement (`src/data/`), normalisation dans [-1, 1], config `configs/data.yaml`.

---

## 2026-08-13 — EDA complète de Fashion-MNIST

- Le notebook `notebooks/01_eda_dataset.ipynb` et l'utilitaire `src/utils/dataset_compare.py` existants étaient un gabarit générique pour comparer des CSV/Parquet, inadapté à des données image — ils ne produisaient pas de rapport exploitable pour Fashion-MNIST/CIFAR-10.
- Ajout de `scripts/eda_fashion_mnist.py` : EDA complète sur le dataset retenu (Fashion-MNIST), couvrant toute la checklist `TASKS.md` (valeurs manquantes, doublons exacts par hash MD5, valeurs aberrantes, équilibre des classes, statistiques de pixels pour la normalisation, échantillon visuel par classe).
- Résultat : dataset propre (0 valeur manquante, 0 doublon exact, pixels dans [0, 255], classes parfaitement équilibrées à 6000/1000 par classe). Rapport lisible dans [`reports/eda_fashion_mnist.md`](reports/eda_fashion_mnist.md), grille d'exemples dans `reports/samples/fashion_mnist_grid.png`.
- Checklist EDA de `TASKS.md` cochée en conséquence.
- **Prochaine étape :** pipeline `src/data/` (Dataset/DataLoader PyTorch, normalisation [-1, 1], split train/éval, config `configs/data.yaml`).

---

## 2026-08-06 — Revue de code (PR #1)

Revue effectuée par AHLI Kossi Sitsofe Pédro, conformément à `CONTRIBUTING.md` (le·la responsable du dossier `data/` ne relit jamais sa propre PR). **Salut Mabelle — voici le détail des points à corriger avant que je (ou Anne) puisse valider le merge sur `master`. Rien de grave, mais plusieurs points sont bloquants car ils rendent des vérifications silencieusement inopérantes plutôt que de planter franchement, ce qui est plus difficile à repérer.**

### Bloquant (à corriger avant merge)

- `scripts/resumable_download.py` : en cas de reprise, le mode d'écriture (`"ab"` vs `"wb"`) est décidé sur la taille du fichier local existant, sans vérifier que le serveur a bien honoré l'en-tête `Range` (code 206). Si le serveur répond `200` avec le contenu complet (repli fréquent sur réseau instable — exactement le cas d'usage visé par ce script), le code **ajoute** ce contenu complet à la suite du fichier partiel déjà présent : fichier `.gz` corrompu, mais accepté comme "téléchargement réussi" faute de vérification de checksum.
- `scripts/resumable_download.py` télécharge uniquement les `.gz` et ne les décompresse jamais, alors que torchvision attend les fichiers IDX décompressés dans `data/raw/FashionMNIST/raw/`. Si ce script sert de repli (cas documenté plus haut dans cet historique), le chargement du dataset échoue quand même ensuite.
- Les contrôles EDA "valeurs manquantes" et "valeurs aberrantes" (`scripts/eda_fashion_mnist.py`) sont vides de sens : ils testent la présence de `NaN` sur un tableau `uint8` (structurellement impossible) et vérifient que les pixels sont dans [0, 255] sur un tableau dont le dtype garantit déjà cette plage. Les cases correspondantes de `TASKS.md` sont cochées, mais ces contrôles ne détecteraient jamais une vraie corruption de données (ex. après une coupure réseau pendant le téléchargement — justement le risque documenté ci-dessus).
- Le notebook `notebooks/01_eda_dataset.ipynb` et `src/utils/dataset_compare.py` ne fonctionnent pas du tout sur ce projet : ils ne gèrent que des fichiers CSV/Parquet, alors que Fashion-MNIST/CIFAR-10 sont des données image (IDX/pickle). L'entrée d'historique ci-dessus l'admet elle-même ("gabarit générique... inadapté à des données image, ne produisait pas de rapport exploitable") mais les fichiers sont quand même ajoutés/conservés tels quels, non fonctionnels — à corriger (les faire fonctionner sur les vraies données) ou à supprimer si `scripts/eda_fashion_mnist.py` les remplace entièrement.
- Imports cassés faute d'ajout de la racine du repo à `sys.path` : `from src.utils.dataset_compare import compare_datasets` échoue avec `ModuleNotFoundError` aussi bien dans le notebook (cwd Jupyter = `notebooks/`) que dans `scripts/compare_datasets.py` (exécuté depuis la racine du repo).
- `requests`, utilisé par `resumable_download.py`, n'est pas déclaré dans `requirements.txt`.

### Précision documentaire

- La case `TASKS.md` "temps d'entraînement estimé sur le matériel disponible" est cochée, mais aucune mesure de temps n'existe dans la PR (`reports/datasets_report.json` ne contient que tailles/formats, pas de benchmark) — soit ajouter une mesure réelle, soit reformuler l'entrée `HISTORY.md` pour ne pas présenter l'estimation comme un chiffre mesuré.
- Petit détail : les dates des entrées `HISTORY.md` ci-dessus (2026-08-13) sont postérieures à la date réelle des commits vus côté horloge du dépôt — probablement l'horloge système de la machine utilisée, à vérifier.

### Qualité / simplification (non bloquant, à considérer si tu as le temps)

- `summarize_dataset()` et `summarize_cifar()` (`scripts/download_and_eda.py`) sont quasi identiques — à fusionner en une seule fonction.
- `scripts/eda_fashion_mnist.py` reconvertit le tableau train `uint8 → float64` à 3-4 reprises séparément (NaN, moyenne, écart-type) — un seul cast réutilisé suffirait (~376 Mo économisés par cast évité).
- `resumable_download.py` est un script à part à invoquer manuellement, avec ses propres URLs redéclarées indépendamment de torchvision — source de vérité qui peut diverger ; à envisager : l'intégrer directement dans `download_and_eda.py`.
- `scripts/download_and_eda.py` avale silencieusement les erreurs de sauvegarde d'échantillons CIFAR (`except Exception: pass`, sans log) — un échantillon manquant passerait inaperçu.
- `src/utils/dataset_compare.py` (si conservé) : plante sur colonnes dupliquées, comparaison d'extension sensible à la casse (`.parquet` vs `.PARQUET`), hash de ligne calculé avant l'échantillonnage plutôt qu'après (travail inutile sur les lignes jetées).

**Statut : PR non mergée.** Une fois les points bloquants corrigés, la review doit être validée par un·e des deux autres membres de l'équipe (pas moi, cf. règle `CONTRIBUTING.md`) avant merge sur `master`.

---

## 2026-08-22 — Corrections suite à la revue de code (PR #1)

Réponse point par point aux points bloquants de la review du 2026-08-06/08-18 :

- `scripts/resumable_download.py` : corrigé le bug de reprise — le mode d'écriture (`ab`/`wb`) dépend désormais du status code réellement renvoyé par le serveur (`206` = reprise honorée, sinon on repart de 0), plus de la seule taille locale. Le script décompresse maintenant lui-même les `.gz`/`.tar.gz` et vérifie le MD5 (mêmes valeurs que `torchvision`) avant extraction — utilisable seul, sans dépendre d'un appel torchvision derrière.
- `scripts/eda_fashion_mnist.py` : suppression des contrôles vides de sens (`NaN`/plage sur `uint8`, structurellement impossibles) ; remplacés par une vérification honnête (intégrité déjà garantie en amont par le checksum MD5 de torchvision au chargement) et un vrai contrôle d'images dégénérées (entièrement uniformes) qui, lui, peut réellement détecter une anomalie malgré un fichier au checksum valide. Un seul cast `uint8 → float64` réutilisé au lieu de plusieurs.
- `notebooks/01_eda_dataset.ipynb`, `src/utils/dataset_compare.py`, `scripts/compare_datasets.py` supprimés : gabarit générique CSV/Parquet non fonctionnel sur des données image, entièrement remplacé par `scripts/eda_fashion_mnist.py`. Remplacés par `notebooks/01_eda_fashion_mnist.ipynb`, qui appelle réellement ce script (import corrigé, plus d'erreur `ModuleNotFoundError`) — exécuté de bout en bout pour vérifier.
- `requests` ajouté à `requirements.txt`.
- `HISTORY.md` : justification du choix du dataset reformulée pour ne pas présenter l'estimation par volume de pixels comme un temps d'entraînement mesuré.
- `scripts/download_and_eda.py` : fusion de `summarize_dataset`/`summarize_cifar` (quasi identiques) en une seule fonction ; l'erreur silencieuse (`except: pass`) sur la sauvegarde d'échantillons CIFAR loggue maintenant un avertissement au lieu de disparaître.
- Dates `HISTORY.md` du 2026-08-13 vérifiées face à l'horodatage Git réel des commits (`git log --date=iso`) : elles correspondent exactement à l'horloge du dépôt à ce moment-là, donc laissées telles quelles.
- Non traité pour l'instant : vérification formelle de la licence Fashion-MNIST/CIFAR-10 (case `TASKS.md` correspondante laissée décochée).

---

## 2026-08-27 — Matière de préparation à la présentation

Travail réalisé sur la branche `aaksp` (non mergé sur `master`), checklist "Présentation" de `TASKS.md` (préparation, pas encore les slides finales ni la répétition chronométrée).

- Ajout de `presentation/` : `concepts_a_comprendre.md` (révision des concepts clés — diffusion forward/inverse, rôle du U-Net et de l'embedding temporel, principe adversarial du GAN, résultat contre-intuitif de l'étude d'ablation, lecture du FID, limites à assumer, questions probables anticipées) et `guide_app_api.md` (guide de la démo live : schéma du flux app↔API, justification du choix d'une API séparée de l'app, rôle de chaque endpoint, déroulé conseillé de la démo, points de vigilance).
- **API et app relancées en local pour vérification** (`uvicorn app.api.main:app --port 8000`, `streamlit run app/web/app.py --server.port 8501`, `API_URL` pointée vers l'API locale) : `/health` confirme les deux modèles chargés depuis les checkpoints existants, une génération GAN via l'API confirme le flux de bout en bout. Docker non utilisé cette fois (Docker Desktop non démarré sur la machine) — l'exécution directe reste équivalente et déjà documentée comme fonctionnelle.
- Note technique : premier lancement de Streamlit sur cette machine bloqué par l'invite d'onboarding interactive (email) ; contournée en pré-remplissant `~/.streamlit/credentials.toml` (`email = ""`).
- **Prochaine étape :** construire les slides à partir de `presentation/concepts_a_comprendre.md`, répéter la démo live avec `presentation/guide_app_api.md`, chronométrer (20 min).
