# configs/

Fichiers de configuration (YAML) décrivant chaque expérience : dataset, hyperparamètres du modèle, seed, nombre de pas de diffusion, etc.

Chaque entrée du tableau d'ablation du rapport doit correspondre à un fichier de config ici, pour que les résultats soient reproductibles avec une seule commande (ex. `python -m src.training.train_ddpm --config configs/ddpm_steps100.yaml`).
