# scripts/

Scripts de reproduction des résultats :

- `prepare_data.py` — télécharge/prépare le dataset à partir d'une config (`configs/data.yaml`).
- `train.py --config <path>` — point d'entrée générique d'entraînement, détecte automatiquement DDPM ou GAN et délègue à `src.training.train_ddpm`/`train_gan`.
- `compare_datasets.py` — script ponctuel ayant servi au choix du dataset (Fashion-MNIST vs CIFAR-10, cf. `HISTORY.md`), conservé pour référence/reproductibilité de cette décision.

Le calcul du FID et des métriques de comparaison DDPM vs GAN se trouve dans `src/evaluation/metrics.py`, utilisé depuis `notebooks/06_evaluation_ddpm_vs_gan.ipynb` (pas encore un script autonome ici).

Objectif : n'importe quel résultat du tableau d'ablation du rapport doit pouvoir être reproduit par une seule commande depuis ce dossier.
