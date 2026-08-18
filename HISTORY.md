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
