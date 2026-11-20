# Projet FAS 

## Membres du groupe
- **EL AMRI Ahmed Amine**
- **Daanoun Yassine**

---

## Description
Ce projet consiste en un jeu interactif basé sur les mouvements de la main et la détection par caméra. Il utilise les bibliothèques OpenCV et Mediapipe pour contrôler les interactions et intégrer la logique du jeu. Le joueur contrôle un personnage (T-Rex) en utilisant des gestes de la main détectés par la caméra.

---

## Fonctionnalités
- **Détection des mains** : Utilisation de Mediapipe pour détecter et suivre les mouvements de la main.
- **Contrôle du personnage** : Le joueur peut faire sauter ou descendre le T-Rex en levant ou en baissant la main.
- **Gestion des obstacles** : Des obstacles apparaissent aléatoirement, et le joueur doit les éviter.
- **Score** : Le score augmente au fil du temps, et le jeu se termine en cas de collision.
- **Effets sonores** : Des sons sont joués pour les actions du joueur (saut, collision, etc.).

---

## Installation

### Prérequis
- **Python 3.7 ou version ultérieure** : Assurez-vous que Python est installé sur votre machine.
- **Git** : Pour cloner le dépôt.

### Étapes d'installation
1. Clonez le dépôt GitLab :
   - git clone https://gitlab.polytech.umontpellier.fr/ahmed-amine.el-amri/fas.git
   - cd fas

2. **Bibliothèques nécessaires** : Installez les dépendances via pip :
   - pip install opencv-python mediapipe
   - pip install pillow
   - pip install simpleaudio






## Utilisation
## Démarrage du jeu

**EXECUTER LE FICHIER main2.py**

Placez-vous devant la caméra et utilisez vos mouvements de main pour contrôler le T-Rex :

1. Lever la main : Fait sauter le T-Rex.
2. Baisser la main : Le T-Rex reste au sol.

## Règles du jeu

- Évitez les obstacles pour augmenter votre score.
- Le jeu se termine en cas de collision avec un obstacle.