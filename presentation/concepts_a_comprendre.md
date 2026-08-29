# Concepts à comprendre avant la présentation

Support de révision — pas un script à lire, mais la matière à maîtriser pour pouvoir expliquer le projet avec ses mots et répondre aux questions. Chiffres et détails sourcés dans `HISTORY.md` et `reports/rapport.docx`.

## 1. Le sujet en une phrase

Comparer deux façons différentes de générer des images (des vêtements Fashion-MNIST) : un modèle de diffusion (DDPM), implémenté **from scratch**, et un GAN (DCGAN), entraînés sur les mêmes données avec un budget de calcul comparable.

## 2. Pourquoi Fashion-MNIST ?

- Pas de GPU sur la machine de dev (CPU uniquement) → il fallait un dataset léger.
- Fashion-MNIST (28×28, niveaux de gris) coûte ~4x moins cher à traiter que CIFAR-10 (32×32, RGB).
- Mais reste assez varié visuellement (10 classes de vêtements, certaines proches — ex. chemise/t-shirt/manteau) pour que la différence de qualité entre DDPM et GAN soit observable.

**Si on te demande "pourquoi pas un dataset plus impressionnant" → réponds budget de calcul, assume-le, c'est un choix documenté, pas une contrainte subie en silence.**

## 3. Le DDPM — comment ça marche

- **Idée centrale** : partir d'une image, la détruire progressivement en ajoutant du bruit gaussien (processus **forward**), puis apprendre à faire l'inverse — retirer le bruit petit bout par petit bout (processus **inverse**) — pour, au final, être capable de partir de bruit pur et « faire apparaître » une image.
- **Formule fermée** : on peut calculer directement l'image bruitée à n'importe quelle étape t sans simuler toutes les étapes intermédiaires (`q(x_t | x_0)`), ce qui rend l'entraînement rapide : à chaque step, on tire un t au hasard, on bruite l'image à ce niveau-là, et on demande au modèle de deviner le bruit ajouté.
- **Le U-Net** : le réseau qui apprend à prédire ce bruit. Il doit aussi savoir *à quel niveau de bruit* on se trouve → c'est le rôle de l'**embedding du temps t** (encodage sinusoïdal, comme dans un Transformer).
- **La loss** : juste une MSE (erreur quadratique) entre le bruit réel et le bruit prédit. Très simple, très stable à entraîner — pas de jeu à deux joueurs comme dans un GAN.
- **La génération (sampling)** : on part d'une image de bruit pur, et on applique le U-Net T fois de suite (un pas de débruitage à chaque fois) pour arriver à une image finale. **C'est pour ça que générer avec un DDPM est lent : autant de passes du réseau que de pas T.**
- **T = nombre de pas de diffusion** : hyperparamètre clé. Notre baseline utilise T=1000 (comme Ho et al. 2020).
- **Pourquoi pas d'attention dans notre U-Net ?** Choix délibéré : l'architecture originale en a, mais ça coûte cher en calcul. Sur CPU, on l'a retirée pour rester entraînable dans un temps raisonnable (~3,54M paramètres au lieu de bien plus).

## 4. Le GAN (DCGAN) — comment ça marche

- **Idée centrale** : deux réseaux s'affrontent. Un **générateur** essaie de produire des images crédibles à partir de bruit aléatoire ; un **discriminateur** essaie de distinguer les vraies images des fausses. Ils s'entraînent en même temps, chacun poussant l'autre à s'améliorer.
- **DCGAN** (Radford et al. 2015) : la version « convolutive stabilisée » du GAN original — BatchNorm, LeakyReLU, pas de couches entièrement connectées. C'est l'architecture qu'on utilise.
- **La génération est instantanée** : une seule passe du générateur suffit (pas de boucle comme le DDPM) — gros avantage en vitesse.
- **Le revers de la médaille : l'instabilité.** Le générateur et le discriminateur peuvent se déséquilibrer (l'un devient trop fort trop vite), ce qui donne des oscillations de loss, voire un **mode collapse** (le générateur ne produit plus qu'un petit nombre de formes, faute de diversité). On a observé de l'instabilité (oscillations, pics de loss) mais **pas de mode collapse total** dans nos runs.
- **Artefacts en damier** : défaut connu des couches `ConvTranspose2d` utilisées dans le générateur (Odena et al. 2016) — visibles sur nos échantillons GAN.

## 5. L'étude d'ablation — le résultat le plus intéressant à raconter

- On a fait varier **T** (100, 400, 1000) en gardant tout le reste identique (architecture, seed, **budget d'entraînement égal** = 500 steps pour les trois).
- Résultat attendu : plus T est grand, plus la génération est lente (confirmé, quasi linéaire).
- **Résultat inattendu** : à budget d'entraînement égal, **T=400 donne les images les plus nettes**, pas T=1000 — alors que T=1000 a la loss la plus basse ! Pourquoi ? Avec un nombre de steps de gradient fixe, plus T est grand, plus chaque valeur de t est vue rarement à l'entraînement → le modèle est relativement sous-entraîné à T élevé. **Loss basse ≠ bonne qualité visuelle** ici, c'est un point important à savoir expliquer.
- Conclusion pratique : sur un budget de calcul limité, il vaut mieux moins de pas de diffusion mais bien entraînés, que beaucoup de pas mal exploités.

## 6. La comparaison chiffrée DDPM vs GAN

- **FID (Fréchet Inception Distance)** : mesure la ressemblance statistique entre la distribution des images générées et celle des images réelles (plus bas = plus proche des vraies images). On l'a calculé sur 100 images par groupe (petit échantillon, donc à interpréter comme une comparaison relative, pas une valeur absolue de référence).
- **Résultat** : DDPM = FID 114 (meilleur), GAN = FID 173.
- **Mais** : le GAN génère ~21 600 fois plus vite (une passe vs 1000 passes). **C'est LE compromis à retenir : qualité (DDPM) contre vitesse (GAN).**
- **Diversité** : pas de doublons quasi-identiques détectés pour aucun des deux modèles ; le GAN a une variance intra-batch légèrement plus faible que le DDPM (moins de diversité, mais pas de collapse).

## 7. Les limites à assumer (si on te les demande, ne les cache pas)

- **Pas de GPU** = facteur limitant central de tout le projet (taille du modèle, nombre de steps, taille des échantillons FID).
- **FID sur seulement 100 images** par groupe (la littérature recommande des milliers) → comparaison relative fiable, valeur absolue à prendre avec des pincettes.
- **Pas de test de stabilité du GAN sur plusieurs seeds** → un seul run, donc la conclusion "GAN plus instable" repose sur un échantillon de taille 1.
- **Ablation à 500 steps d'entraînement** (pas 1000 comme la baseline) → le résultat "T=400 meilleur que T=1000" pourrait être en partie un artefact de ce budget réduit.

## 8. Questions probables et pistes de réponse

- *"Pourquoi le DDPM est-il si lent ?"* → Génération = boucle de T pas de débruitage, chacun une passe complète du U-Net.
- *"Le GAN est instable, ça veut dire quoi concrètement ?"* → Les loss du générateur et du discriminateur oscillent au lieu de converger doucement ; dans le pire cas ça peut mener au mode collapse (pas observé ici).
- *"C'est quoi le schedule de bruit β_t ?"* → La vitesse à laquelle on ajoute du bruit à chaque étape du processus forward ; on a utilisé un schedule linéaire (Ho et al. 2020), un schedule cosine existe aussi dans le code mais n'a pas été retenu pour la baseline.
- *"Le FID de 114 c'est bien ou pas ?"* → Pas comparable en absolu à la littérature (échantillon trop petit) ; ce qui compte c'est que le DDPM fait mieux que le GAN **dans les mêmes conditions**.
- *"Qu'auriez-vous fait avec un GPU/plus de temps ?"* → Plus de steps d'entraînement (baseline et ablation), FID sur plusieurs milliers d'images, plusieurs seeds pour la stabilité du GAN, un U-Net avec attention.
- *"Pourquoi une API séparée de l'app ?"* → cf. `guide_app_api.md`.
