# Guide de présentation — App & API (démo live)

Ce que fait chaque brique, pourquoi elle existe, et comment enchaîner la démo devant le jury.

## Vue d'ensemble du flux

```
Utilisateur (navigateur)
      │  clique "Générer"
      ▼
App Streamlit (port 8501)
      │  requête HTTP GET /generate?model=ddpm|gan&n=...
      ▼
API FastAPI (port 8000)
      │  modèles DDPM + GAN déjà chargés en mémoire (une fois, au démarrage)
      │  génère n images
      ▼
Réponse JSON {model, n, images: [PNG en base64, ...]}
      ▼
Streamlit décode les PNG et les affiche
```

Deux services séparés (API + app), orchestrés soit directement (`uvicorn` + `streamlit run`), soit via Docker (`docker compose up --build`).

## Pourquoi une API séparée de l'app ? (question à anticiper)

C'est le point le plus susceptible d'être demandé — ne pas le survoler.

- **Séparation des responsabilités** : l'API porte toute la logique lourde (PyTorch, modèles, génération) ; l'app ne fait qu'afficher et appeler l'API. Chacune peut évoluer, être testée, ou plantée indépendamment.
- **Le modèle est chargé une seule fois**, au démarrage de l'API (`lifespan` FastAPI) — pas à chaque clic sur "Générer". Recharger un modèle PyTorch à chaque requête serait beaucoup plus lent.
- **Réutilisabilité** : n'importe quel client peut consommer les mêmes endpoints — l'app Streamlit, mais aussi un script Python, une appli mobile, un autre service, `curl`. On ne duplique pas la logique de génération pour chaque interface.
- **Découplage du déploiement** : dans un vrai contexte de production, l'API (calcul lourd, potentiellement sur une machine avec GPU) et l'app (interface légère) pourraient tourner sur des machines différentes. C'est la raison pour laquelle Docker les traite comme deux services indépendants.
- **Standard de l'industrie** : séparer le "moteur ML" (API) du "produit" (interface) est le patron classique pour tout service ML exposé publiquement — pas une complexité gratuite, une architecture réutilisée partout.

## Ce que fait l'API (`app/api/main.py`)

- **`GET /health`** : renvoie le statut et la liste des modèles effectivement chargés. Utile pour vérifier que tout est prêt avant de lancer la démo (à montrer en premier, très rapide).
- **`GET /generate?model=ddpm|gan&n=...`** : génère `n` images avec le modèle demandé.
  - `model` : validé strictement (seulement `"ddpm"` ou `"gan"` acceptés) → réponse `422` sinon.
  - `n` : plafonné par modèle (`4` pour DDPM, `16` pour GAN — le DDPM est coûteux en CPU, ~18,5 s/image) → réponse `400` si dépassé.
  - Si un modèle n'a pas pu être chargé (checkpoint absent) → réponse `503`, pas un plantage silencieux.
  - Réponse : JSON avec les images encodées en base64/PNG (format texte, transportable simplement sur HTTP, pas besoin de gérer des fichiers).

## Ce que fait l'app (`app/web/app.py`)

- Sélecteur de modèle : **DDPM**, **GAN**, ou **comparaison côte à côte**.
- Slider du nombre d'images (borné aux mêmes limites que l'API).
- Bouton "Générer" → appelle l'API (bibliothèque `requests`), décode les images reçues, les affiche.
- Bloc de métriques à chaque génération : **FID de référence** (mesuré une fois pour toutes dans `notebooks/06_evaluation_ddpm_vs_gan.ipynb`, pas recalculé en direct — trop coûteux) et **temps de génération mesuré en direct** sur la requête en cours.

## Pourquoi Docker par-dessus ?

- **Portabilité** : `docker compose up --build` suffit, sans installer Python/PyTorch/etc. à la main sur une autre machine.
- **Isolation** : chaque service a son propre environnement, pas de conflit de dépendances entre l'API et l'app.
- **Les checkpoints entraînés sont montés en volume**, pas copiés dans l'image : ils sont trop lourds et non versionnés dans Git (cf. `.gitignore`). Il faut donc les avoir déjà générés localement (`python scripts/train.py --config ...`) avant de lancer les conteneurs.

## Déroulé conseillé pour la démo live

1. **`/health`** (navigateur ou `curl`) → montrer que les deux modèles sont chargés. Rapide, rassurant, montre que l'infra tourne.
2. **App Streamlit, mode GAN** → cliquer "Générer" : quasi instantané. Bon point d'entrée, ça ne fait pas attendre le jury.
3. **App Streamlit, mode DDPM** → cliquer "Générer" : **prévenir avant de cliquer que ça prend ~15-20 secondes par image** (1000 passes du U-Net) — évite un silence gênant, et c'est l'occasion d'expliquer pourquoi (cf. `concepts_a_comprendre.md`, section DDPM).
4. **Mode "Comparaison côte à côte"** → montrer les deux résultats en parallèle avec les métriques affichées (FID de référence, temps mesuré) : c'est le moment de résumer le compromis qualité (DDPM) vs vitesse (GAN).
5. **Filet de sécurité** : si la démo live plante (réseau, port déjà pris, etc.), avoir les captures déjà disponibles dans `reports/figures/` (`ddpm_baseline_samples.png`, `gan_baseline_samples.png`, `eval_real_ddpm_gan.png`) prêtes à montrer à la place.

## Points de vigilance avant de présenter

- Lancer l'API et l'app **avant** de commencer à parler (démarrage = quelques secondes, le temps de charger les checkpoints) — ne pas le faire devant le jury.
- Vérifier `/health` en premier dans les coulisses : si un modèle manque, le régénérer avec `python scripts/train.py --config configs/ddpm_base.yaml` (ou `gan_base.yaml`) avant la présentation.
- Un seul DDPM à la fois pendant la démo (max 4 images) pour ne pas faire attendre inutilement — la vitesse du GAN est plus impressionnante en live, garder le DDPM pour illustrer la qualité, pas la rapidité.
