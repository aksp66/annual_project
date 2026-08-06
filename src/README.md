# src/

Code source du projet, organisé par responsabilité.

- `data/` — chargement et prétraitement du dataset retenu (Fashion-MNIST, cf. `HISTORY.md` pour la comparaison à CIFAR-10), transforms, dataloaders.
- `models/ddpm/` — U-Net de débruitage, processus de diffusion direct/inverse (from scratch).
- `models/gan/` — générateur et discriminateur (DCGAN).
- `training/` — boucles d'entraînement DDPM et GAN, gestion des seeds et des configs.
- `evaluation/` — métriques (FID, temps de génération), scripts de comparaison DDPM vs GAN.
- `utils/` — fonctions communes (seed fixe, logging, checkpointing).

Chaque script d'entraînement doit être reproductible (seed fixé, config versionnée dans `configs/`).
