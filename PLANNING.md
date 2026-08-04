# Planning de travail

Plan calé sur le fil rouge du cours : 14 séances de 2h (28h), réparties en 4 phases (cf. slides p.28). Les rôles sont ceux définis dans [`CONTRIBUTING.md`](CONTRIBUTING.md) : **Data/Experiment Engineer (Data)**, **Model/Research Engineer (Model)**, **Reporting/Backend Developer (Backend)**. Tant que l'attribution nominative n'est pas faite, ce plan reste par rôle.

Méthode : avancer par tranches verticales (un mini bout-en-bout qui marche tôt, puis on améliore) plutôt que tout finir un module avant de passer au suivant. Chaque tâche terminée est loguée dans [`HISTORY.md`](HISTORY.md).

> Le choix définitif du dataset (Fashion-MNIST vs CIFAR-10 downscalé) n'est pas encore tranché — c'est la première tâche de la Phase 1, elle conditionne les temps d'entraînement estimés ci-dessous.

## Phase 1 — Cadrage (S1-S2, ~4h)

|Tâche|Rôle|Durée|Livrable|
|---|---|---|---|
|Choix du dataset (volume, résolution, budget de calcul dispo)|Data|1h|Décision actée dans `HISTORY.md`|
|Lecture des papiers de référence (DDPM — Ho et al. 2020 ; GAN — Goodfellow et al. 2014)|Model|2h|Synthèse pour la section "Travaux liés" du rapport|
|Répartition définitive des rôles, tableau Équipe complété|Tous|1h|`Readme.md` à jour|
|Structure repo, `CONTRIBUTING.md`, planning|Backend|fait|Repo prêt|

## Phase 2 — Données + Modèle (S3-S7, ~10h)

|Tâche|Rôle|Durée|Livrable|
|---|---|---|---|
|EDA du dataset choisi (distributions, exemples, volumétrie)|Data|2h|Notebook dans `notebooks/`|
|Pipeline de chargement/prétraitement (dataloader, normalisation, resize) + config|Data|2h|`src/data/`, `configs/data.yaml`|
|Processus de diffusion direct (bruitage) — from scratch|Model|1h|`src/models/ddpm/`|
|U-Net de débruitage + processus inverse|Model|3h|`src/models/ddpm/`|
|Entraînement DDPM baseline (config par défaut)|Model|2h|`experiments/ddpm_baseline/`|
|DCGAN (générateur + discriminateur)|Model|2h|`src/models/gan/`|
|Entraînement GAN baseline (budget comparable au DDPM)|Model|1h|`experiments/gan_baseline/`|
|**Étude d'ablation** : nombre de pas de diffusion (≥3 configs, ex. 100/400/1000)|Model + Data (scripts repro)|2h|`configs/ddpm_steps*.yaml`, tableau de résultats|
|Métriques (FID ou évaluation qualitative structurée, temps de génération)|Model|1h|`src/evaluation/`|
|Rédaction continue : sections Données + Méthode du rapport|Backend|en continu|`reports/`|

## Phase 3 — API + App + Docker (S8-S11, ~8h)

|Tâche|Rôle|Durée|Livrable|
|---|---|---|---|
|API FastAPI (charge les 2 modèles, endpoint de génération)|Backend|3h|`app/api/`|
|App Streamlit (génération côte à côte DDPM/GAN)|Backend|2h|`app/web/`|
|Dockerfiles (api, app) + `docker-compose.yml`|Backend|2h|`docker/`|
|Intégration des modèles finaux (post-ablation) dans l'app|Model + Backend|1h|App fonctionnelle de bout en bout|

## Phase 4 — Finalisation (S12-S14, ~6h)

|Tâche|Rôle|Durée|Livrable|
|---|---|---|---|
|Comparaison finale chiffrée DDPM vs GAN + analyse de stabilité d'entraînement|Model|2h|Tableau comparatif dans le rapport|
|Rédaction complète du rapport (ablation, résultats, discussion/limites, répartition du travail)|Tous (Backend pilote)|2h|`reports/rapport.pdf`|
|Préparation de la présentation (slides + démo live)|Tous|1h|Support de présentation|
|Relecture finale + test de reproductibilité (`docker compose up --build`, scripts)|Tous|1h|Repo validé|
|Envoi rapport + code|Backend|—|tchaye59@gmail.com, avant dernière séance|

## Charge totale estimée par rôle

|Rôle|Heures estimées|
|---|---|
|Data|~5h|
|Model|~14h|
|Backend|~9h|

Charge indicative pour équilibrer la répartition — à ajuster une fois les rôles nommément attribués et le dataset tranché.
