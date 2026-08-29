# configs/

Fichiers de configuration (YAML) décrivant chaque expérience : dataset, hyperparamètres du modèle, seed, nombre de pas de diffusion, etc.

Chaque entrée du tableau d'ablation du rapport correspond à un fichier de config ici (`ddpm_ablation_steps100.yaml`, `ddpm_ablation_steps400.yaml`, `ddpm_ablation_steps1000.yaml`), pour que les résultats soient reproductibles avec une seule commande : `python scripts/train.py --config configs/ddpm_ablation_steps100.yaml` (ou `python -m src.training.train_ddpm --config ...`).
