# Contribuer au projet

## Branches

`master` reste toujours stable et fonctionnel — on n'y pousse jamais directement.

Une branche courte par tâche, préfixée par domaine :

|Préfixe|Usage|Exemple|
|---|---|---|
|`data/`|EDA, chargement, prétraitement|`data/eda-fashion-mnist`|
|`model/`|Architecture DDPM / GAN|`model/ddpm-unet`, `model/gan-dcgan`|
|`exp/`|Entraînements, étude d'ablation|`exp/ablation-diffusion-steps`|
|`app/`|API, interface web|`app/api-fastapi`, `app/web-streamlit`|
|`docker/`|Conteneurisation|`docker/compose-setup`|
|`docs/`|Rapport, README, historique|`docs/rapport-methode`|

## Responsabilités par dossier

GitHub ne permet pas de restreindre l'accès à un sous-dossier au sein d'un même repo : chaque membre a accès en écriture à tout. Le tableau ci-dessous fixe donc un **responsable principal** par domaine — la personne prioritaire pour relire/merger les PR qui le touchent, pas une barrière technique. N'importe qui peut proposer une PR sur n'importe quel dossier.

|Dossier|Responsable principal|Rôle|
|---|---|---|
|`data/`, `src/data/`, `notebooks/` (EDA)|KOYE Leleda Ma Belle (`Mabelle95`) — Data / Experiment Engineer|Collecte, prétraitement, exploration des données|
|`src/models/ddpm/`, `src/models/gan/`, `src/training/`, `experiments/`|AHLI Kossi Sitsofe Pédro (`aksp66`) — Model / Research Engineer|Architectures, entraînement, résultats bruts|
|`src/evaluation/`, `configs/`|`aksp66` (avec `Mabelle95`)|Métriques, étude d'ablation, définition des expériences|
|`app/`, `docker/`|KONTEVI Akossiwa Anne (`anne952`) — Reporting / Backend Developer|API, interface de démo, conteneurisation|
|`reports/`|`anne952`|Rédaction du rapport (contenu alimenté par toute l'équipe)|
|`scripts/`, `src/utils/`, `tests/`|Transverse|Reproductibilité, code partagé — pas de propriétaire unique|
|`project/`, `Readme.md`, `HISTORY.md`, `CONTRIBUTING.md`|Transverse|Documentation du projet, à jour par tous|

Un fichier [`.github/CODEOWNERS`](.github/CODEOWNERS) reprend cette table pour que GitHub demande automatiquement la review du bon responsable sur chaque PR.

**Règle de review :** le·la responsable d'un dossier ne relit jamais sa propre PR. Comme l'équipe compte 3 personnes, quand l'auteur·e est justement responsable du domaine touché, la review revient à l'un·e des deux autres membres (peu importe lequel·le — pas de binôme fixe nécessaire à cette taille d'équipe).

## Workflow

1. Créer la branche depuis `master` à jour : `git checkout master && git pull && git checkout -b model/ddpm-unet`.
2. Committer par petites étapes logiques, messages clairs (à l'impératif, ex. `Ajoute le forward process de diffusion`).
3. Pousser la branche et ouvrir une Pull Request vers `master`.
4. Faire relire par au moins un·e autre membre de l'équipe avant de merger (même rapide — ça sert aussi de trace pour la section "répartition du travail" du rapport).
5. Merger, puis supprimer la branche.

## Reproductibilité

Toute PR qui touche à l'entraînement (DDPM, GAN) doit :
- fixer un seed,
- s'appuyer sur un fichier de config dans `configs/` (pas de hyperparamètres en dur dans le code),
- être lançable par une seule commande depuis `scripts/`.

## Historique

Toute action notable (nouvelle brique, résultat d'ablation, décision d'équipe) doit être ajoutée à [`HISTORY.md`](HISTORY.md).
