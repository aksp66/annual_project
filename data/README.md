# data/

Données du projet — **non versionnées** dans Git (voir `.gitignore`), régénérées via les scripts de `scripts/`.

- `raw/` — données brutes telles que téléchargées (Fashion-MNIST ; `cifar-10-*` également présent, issu de la comparaison de datasets, cf. `HISTORY.md` — non utilisé depuis la décision).
- `processed/` — **actuellement inutilisé** : le pipeline (`src/data/dataset.py`) applique le padding et la normalisation à la volée dans le `DataLoader`, sans rien matérialiser sur disque. Ce dossier reste réservé si une étape de prétraitement à part devenait nécessaire.

Téléchargement/préparation reproductible via `scripts/prepare_data.py --config configs/data.yaml`.
