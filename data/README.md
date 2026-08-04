# data/

Données du projet — **non versionnées** dans Git (voir `.gitignore`), régénérées via les scripts de `scripts/`.

- `raw/` — données brutes telles que téléchargées (ex. Fashion-MNIST, CIFAR-10).
- `processed/` — données prétraitées (resize, normalisation) prêtes pour l'entraînement.

Le script de téléchargement/préparation doit être documenté dans `scripts/` pour que le pipeline soit reproductible.
