# Soutenance - DDPM from scratch vs. GAN

Projet 3 - Modèle de diffusion entraîné from scratch vs. GAN  
Dataset : Fashion-MNIST  
Durée cible : 20 minutes

---

## 1. Contexte et objectif - 2 min

- Comparer deux familles de modèles génératifs : DDPM et GAN.
- Même dataset, même cadre expérimental, budget de calcul limité sur CPU.
- Question centrale : quel compromis entre qualité visuelle, diversité, stabilité et coût de génération ?

Message clé : le DDPM est plus stable et donne un meilleur score FID dans notre protocole, mais il est beaucoup plus lent à générer.

---

## 2. Dataset et préparation - 2 min

- Dataset retenu : Fashion-MNIST.
- 60 000 images train, 10 000 images test, 10 classes équilibrées.
- Images en niveaux de gris, format initial 28x28.
- Padding vers 32x32 pour simplifier les descentes/remontées du U-Net.
- Normalisation dans [-1, 1], compatible DDPM et GAN.

À montrer : `reports/figures/eda_samples.png` et `reports/figures/eda_classes.png`.

---

## 3. Méthode DDPM - 4 min

- Processus direct : ajout progressif de bruit gaussien selon un schedule linéaire.
- Formule fermée de bruitage `q(x_t | x_0)` implémentée from scratch.
- Processus inverse : apprentissage du débruitage avec un petit U-Net.
- Loss : MSE entre le bruit réel et le bruit prédit.
- Sampling : départ depuis un bruit pur, puis débruitage étape par étape.

À montrer : `reports/figures/forward_noising.png`.

Point important : le DDPM nécessite plusieurs passes séquentielles du U-Net à la génération.

---

## 4. Méthode GAN/DCGAN - 3 min

- Générateur : bruit latent vers image 32x32 via convolutions transposées.
- Discriminateur : classification réel/faux avec convolutions et LeakyReLU.
- Loss adversariale `BCEWithLogitsLoss`.
- Alternance entraînement discriminateur puis générateur.
- Suivi de `loss_g`, `loss_d`, `D(real)` et `D(fake)`.

Point important : le GAN génère en une seule passe, mais l'entraînement est plus instable.

---

## 5. Étude d'ablation - 3 min

Variable étudiée : nombre de pas de diffusion `T`.

| T | Temps entraînement | Temps génération 8 images | Loss finale |
|---|---:|---:|---:|
| 100 | 3295,7 s | 13,4 s | 0,1107 |
| 400 | 3667,6 s | 52,0 s | 0,0648 |
| 1000 | 3777,2 s | 128,4 s | 0,0430 |

À montrer : `reports/figures/ablation_gentime_loss.png` et `reports/figures/ablation_samples.png`.

Conclusion : augmenter `T` améliore la loss de débruitage, mais augmente fortement le temps de génération.

---

## 6. Résultats DDPM vs GAN - 3 min

| Métrique | DDPM | GAN |
|---|---:|---:|
| FID vs réel | 114,12 | 173,47 |
| Variance intra-batch | 0,2443 | 0,2292 |
| Quasi-doublons | 0 | 0 |
| Temps génération 100 images | 1854,0 s | 0,09 s |

À montrer : `reports/figures/eval_real_ddpm_gan.png`.

Lecture des résultats :

- DDPM : meilleure qualité relative dans notre protocole, génération très lente.
- GAN : génération quasi instantanée, mais artefacts plus visibles et entraînement oscillant.
- FID calculé sur 100 images : interprétation relative, pas comparaison absolue à la littérature.

---

## 7. Démonstration - 2 min

Commandes :

```bash
docker compose up --build
```

Puis ouvrir :

- API FastAPI : `http://localhost:8000/health`
- Application Streamlit : `http://localhost:8501`

Scénario de démonstration :

1. Vérifier que l'API voit les checkpoints.
2. Générer une image GAN seule pour montrer la rapidité.
3. Générer une image DDPM seule pour montrer le coût de génération.
4. Utiliser le mode comparaison côte à côte.
5. Commenter FID, temps mesuré et différences visuelles.

Plan de secours :

- Montrer les figures déjà générées dans `reports/figures/`.
- Expliquer que les checkpoints sont nécessaires dans `experiments/*_baseline/checkpoints/`.

---

## 8. Limites et améliorations - 1 min

- Entraînement limité par le CPU : seulement 1000 steps pour les baselines.
- FID calculé sur 100 images, donc bruité.
- Stabilité GAN observée sur un seul seed principal.
- Pas d'auto-attention dans le U-Net, choix volontaire pour réduire le coût.

Améliorations possibles :

- Plusieurs seeds pour comparer la stabilité.
- Plus d'images pour le FID.
- Entraînement plus long sur GPU.
- U-Net avec attention ou schedule de bruit plus avancé.

---

## 9. Répartition du travail - 1 min

- Data : choix Fashion-MNIST, EDA, préparation et vérification des données.
- Model : DDPM, U-Net, DCGAN, entraînements, ablation et métriques.
- Reporting / Backend : API, app web, Docker, rapport, préparation de la soutenance.

Cette soutenance met en avant les livrables attendus : démarche expérimentale, ablation, comparaison chiffrée et démo applicative.
