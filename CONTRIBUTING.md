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
