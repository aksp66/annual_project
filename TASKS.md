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

### Pipeline de chargement / prétraitement
- [x] Écrire le `Dataset`/`DataLoader` PyTorch (`src/data/`)
- [x] Normalisation adaptée à la diffusion (ex. pixels dans [-1, 1])
- [x] Resize/crop si nécessaire (ex. CIFAR-10 downscalé)
- [x] Split train / éval (pour calcul du FID), seed fixé
- [x] Config YAML du pipeline (`configs/data.yaml` : batch size, resize, normalisation)
- [x] Test unitaire : shape et plage de valeurs en sortie du DataLoader

### Scripts de reproductibilité
- [ ] Script de téléchargement/préparation automatique du dataset (`scripts/`)
- [ ] Script générique pour lancer un entraînement à partir d'une config (`scripts/train.py --config ...`)
- [ ] Vérifier qu'un même seed + config reproduit les mêmes résultats

---

## Model / Research Engineer

### Processus de diffusion (forward) — from scratch
- [ ] Choisir et implémenter le schedule de bruit β_t (linéaire, ou cosine)
- [ ] Implémenter la formule fermée q(x_t | x_0) (bruitage direct sans boucle)
- [ ] Vérifier visuellement le bruitage progressif sur quelques images
- [ ] Vérifier que x_T est proche d'un bruit gaussien pur

### U-Net de débruitage + processus inverse
- [ ] Définir l'architecture U-Net (blocs conv, skip connections, downsampling/upsampling)
- [ ] Implémenter l'embedding sinusoïdal du pas de temps t
- [ ] Implémenter la loss (MSE entre bruit prédit et bruit réel)
- [ ] Implémenter la boucle d'échantillonnage (sampling ancestral, x_T → x_0)
- [ ] Tester les shapes sur un batch avant l'entraînement complet
- [ ] Sauvegarder des échantillons générés à intervalles réguliers pendant l'entraînement

### DCGAN
- [ ] Définir l'architecture du générateur (conv transposées, batchnorm, activations)
- [ ] Définir l'architecture du discriminateur (conv, LeakyReLU)
- [ ] Implémenter la loss adversariale (BCE) et les optimizers (Adam, β1=0.5)
- [ ] Implémenter la boucle d'entraînement (alternance générateur/discriminateur)
- [ ] Suivre les courbes de loss G/D pour repérer un éventuel mode collapse

### Entraînement baseline (DDPM + GAN)
- [ ] Fixer seed, config, budget d'entraînement comparable entre les deux modèles
- [ ] Lancer les deux entraînements baseline
- [ ] Sauvegarder les checkpoints régulièrement
- [ ] Logger les courbes de loss (CSV + matplotlib, ou tensorboard)

### Étude d'ablation (nombre de pas de diffusion)
- [ ] Définir ≥3 configs (ex. 100 / 400 / 1000 pas) dans `configs/`
- [ ] Lancer chaque config avec le même seed/dataset
- [ ] Mesurer temps d'entraînement et temps de génération par config
- [ ] Comparer la qualité (visuelle et/ou FID) par config
- [ ] Rédiger le tableau comparatif (base de la section "Étude d'ablation" du rapport)

### Évaluation et comparaison DDPM vs GAN
- [ ] Implémenter/adapter le calcul du FID (`torchmetrics` ou implémentation simplifiée)
- [ ] Mesurer la diversité des échantillons générés (variance intra-batch, doublons visuels)
- [ ] Chronométrer le temps de génération (DDPM multi-pas vs GAN one-shot)
- [ ] Documenter la stabilité d'entraînement du GAN sur plusieurs seeds (oscillations, mode collapse) vs celle du DDPM

---

## Reporting / Backend Developer

### API (FastAPI)
- [ ] Charger les deux modèles (DDPM, GAN) une fois au démarrage
- [ ] Endpoint(s) de génération (ex. `/generate?model=ddpm|gan`)
- [ ] Validation des entrées (Pydantic), codes HTTP appropriés
- [ ] Retour JSON (image encodée base64 ou chemin)
- [ ] Gestion des erreurs (modèle non chargé, paramètre invalide)
- [ ] Tester l'API manuellement (ou tests automatisés légers)

### Application web (Streamlit)
- [ ] Sélecteur de modèle (DDPM / GAN)
- [ ] Bouton de génération + affichage de l'image
- [ ] Affichage côte à côte DDPM vs GAN
- [ ] Affichage indicatif des métriques (FID, temps de génération)
- [ ] Appel à l'API (`requests`)

### Docker
- [ ] Dockerfile pour l'API
- [ ] Dockerfile pour l'app web
- [ ] `docker-compose.yml` orchestrant les deux services
- [ ] Vérifier que `docker compose up --build` fonctionne de bout en bout
- [ ] Documenter ports/variables d'environnement dans `Readme.md`

### Rapport (style article scientifique)
- [ ] Introduction (contexte, problématique, contribution)
- [ ] Travaux liés (synthèse des papiers de référence + apports Model)
- [ ] Données (synthèse EDA + apports Data)
- [ ] Méthode (description précise des modèles, hyperparamètres, protocole)
- [ ] Étude d'ablation (tableau + discussion, apports Model)
- [ ] Résultats (comparaison chiffrée, analyse critique)
- [ ] Déploiement (API, app, Docker)
- [ ] Discussion et limites
- [ ] Répartition du travail (contributions précises de chaque membre)
- [ ] Mise en page finale (8-20 pages, figures/tableaux numérotés)

### Présentation
- [ ] Construire les slides (contexte, méthode, ablation, résultats, démo)
- [ ] Préparer la démo live (app fonctionnelle)
- [ ] Répétition chronométrée (20 minutes)
