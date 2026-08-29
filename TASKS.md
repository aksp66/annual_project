# Détail des tâches par rôle et fonctionnalité

Décompose chaque fonctionnalité de [`PLANNING.md`](PLANNING.md) en actions concrètes. À cocher au fur et à mesure ; toute fonctionnalité terminée est loguée dans [`HISTORY.md`](HISTORY.md).

---

## Data / Experiment Engineer

### Choix du dataset
- [x] Comparer Fashion-MNIST vs CIFAR-10 downscalé (volume, résolution, temps d'entraînement estimé sur le matériel disponible)
- [x] Vérifier la licence et la disponibilité (`torchvision.datasets`)
- [x] Tester le téléchargement et le chargement en local
- [x] Documenter la décision et sa justification dans `HISTORY.md`

### EDA (analyse exploratoire)
- [x] Charger train/test, vérifier les tailles et le format (dimensions, canaux, dtype)
- [x] Rechercher les valeurs manquantes / fichiers corrompus ou illisibles
- [x] Détecter les valeurs aberrantes (images de dimensions incohérentes, pixels hors plage attendue [0, 255])
- [x] Détecter les doublons exacts (hash d'image)
- [x] Analyser l'équilibre des classes (`value_counts`)
- [x] Calculer les statistiques descriptives (moyenne/écart-type des pixels, utile pour la normalisation)
- [x] Visualiser un échantillon d'images par classe
- [x] Consigner les observations (biais, qualité) — base de la section "Données" du rapport

Résultat : [`reports/eda_fashion_mnist.md`](reports/eda_fashion_mnist.md) (`scripts/eda_fashion_mnist.py`).

### Pipeline de chargement / prétraitement
- [x] Écrire le `Dataset`/`DataLoader` PyTorch (`src/data/`)
- [x] Normalisation adaptée à la diffusion (ex. pixels dans [-1, 1])
- [x] Resize/crop si nécessaire (ex. CIFAR-10 downscalé)
- [x] Split train / éval (pour calcul du FID), seed fixé
- [x] Config YAML du pipeline (`configs/data.yaml` : batch size, resize, normalisation)
- [x] Test unitaire : shape et plage de valeurs en sortie du DataLoader

### Scripts de reproductibilité
- [x] Script de téléchargement/préparation automatique du dataset (`scripts/`)
- [x] Script générique pour lancer un entraînement à partir d'une config (`scripts/train.py --config ...`)
- [x] Vérifier qu'un même seed + config reproduit les mêmes résultats

---

## Model / Research Engineer

### Processus de diffusion (forward) — from scratch
- [x] Choisir et implémenter le schedule de bruit β_t (linéaire, ou cosine)
- [x] Implémenter la formule fermée q(x_t | x_0) (bruitage direct sans boucle)
- [x] Vérifier visuellement le bruitage progressif sur quelques images
- [x] Vérifier que x_T est proche d'un bruit gaussien pur

### U-Net de débruitage + processus inverse
- [x] Définir l'architecture U-Net (blocs conv, skip connections, downsampling/upsampling)
- [x] Implémenter l'embedding sinusoïdal du pas de temps t
- [x] Implémenter la loss (MSE entre bruit prédit et bruit réel)
- [x] Implémenter la boucle d'échantillonnage (sampling ancestral, x_T → x_0)
- [x] Tester les shapes sur un batch avant l'entraînement complet
- [x] Sauvegarder des échantillons générés à intervalles réguliers pendant l'entraînement

### DCGAN
- [x] Définir l'architecture du générateur (conv transposées, batchnorm, activations)
- [x] Définir l'architecture du discriminateur (conv, LeakyReLU)
- [x] Implémenter la loss adversariale (BCE) et les optimizers (Adam, β1=0.5)
- [x] Implémenter la boucle d'entraînement (alternance générateur/discriminateur)
- [x] Suivre les courbes de loss G/D pour repérer un éventuel mode collapse

### Entraînement baseline (DDPM + GAN)
- [x] Fixer seed, config, budget d'entraînement comparable entre les deux modèles
- [x] Lancer les deux entraînements baseline
- [x] Sauvegarder les checkpoints régulièrement
- [x] Logger les courbes de loss (CSV + matplotlib, ou tensorboard)

### Étude d'ablation (nombre de pas de diffusion)
- [x] Définir ≥3 configs (ex. 100 / 400 / 1000 pas) dans `configs/`
- [x] Lancer chaque config avec le même seed/dataset
- [x] Mesurer temps d'entraînement et temps de génération par config
- [x] Comparer la qualité (visuelle et/ou FID) par config
- [x] Rédiger le tableau comparatif (base de la section "Étude d'ablation" du rapport)

### Évaluation et comparaison DDPM vs GAN
- [x] Implémenter/adapter le calcul du FID (`torchmetrics` ou implémentation simplifiée)
- [x] Mesurer la diversité des échantillons générés (variance intra-batch, doublons visuels)
- [x] Chronométrer le temps de génération (DDPM multi-pas vs GAN one-shot)
- [ ] Documenter la stabilité d'entraînement du GAN sur plusieurs seeds (oscillations, mode collapse) vs celle du DDPM

---

## Reporting / Backend Developer

### API (FastAPI)
- [x] Charger les deux modèles (DDPM, GAN) une fois au démarrage
- [x] Endpoint(s) de génération (ex. `/generate?model=ddpm|gan`)
- [x] Validation des entrées (Pydantic), codes HTTP appropriés
- [x] Retour JSON (image encodée base64 ou chemin)
- [x] Gestion des erreurs (modèle non chargé, paramètre invalide)
- [x] Tester l'API manuellement (ou tests automatisés légers)

### Application web (Streamlit)
- [x] Sélecteur de modèle (DDPM / GAN)
- [x] Bouton de génération + affichage de l'image
- [x] Affichage côte à côte DDPM vs GAN
- [x] Affichage indicatif des métriques (FID, temps de génération)
- [x] Appel à l'API (`requests`)

### Docker
- [x] Dockerfile pour l'API
- [x] Dockerfile pour l'app web
- [x] `docker-compose.yml` orchestrant les deux services
- [x] Vérifier que `docker compose up --build` fonctionne de bout en bout
- [x] Documenter ports/variables d'environnement dans `Readme.md`

### Rapport (style article scientifique)
- [x] Introduction (contexte, problématique, contribution)
- [x] Travaux liés (synthèse des papiers de référence + apports Model)
- [x] Données (synthèse EDA + apports Data)
- [x] Méthode (description précise des modèles, hyperparamètres, protocole)
- [x] Étude d'ablation (tableau + discussion, apports Model)
- [x] Résultats (comparaison chiffrée, analyse critique)
- [x] Déploiement (API, app, Docker)
- [x] Discussion et limites
- [ ] Répartition du travail (contributions précises de chaque membre) — premier jet honnête rédigé, à mettre à jour une fois les apports de `Mabelle95`/`anne952` intégrés
- [ ] Mise en page finale (8-20 pages, figures/tableaux numérotés) — figures/tableaux déjà numérotés, décompte de pages et relecture finale à faire

### Présentation
- [ ] Construire les slides (contexte, méthode, ablation, résultats, démo)
- [ ] Préparer la démo live (app fonctionnelle)
- [ ] Répétition chronométrée (20 minutes)
