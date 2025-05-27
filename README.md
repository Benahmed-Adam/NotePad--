# NotePad--

NotePad-- est un éditeur de haute qualité écrit en Python à l'aide `pygame`et `pyvidplayer2`. Il est conçu pour redéfinir la façon dont on écrit du texte. 
Avec NotePad--, écrire du texte n'aura jamais été aussi épique.

## Table des matières

- [Fonctionnalités](#fonctionnalités)
- [Dépendances](#dépendances)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Structure du projet](#structure-du-projet)
- [Compatibilité Système](#compatibilité-système)
- [Licence](#licence)
- [Contact](#contact)

## Fonctionnalités

- Édition de texte simple et rapide
- Interface graphique via `pygame`
- Support de la lecture vidéo/audio intégrée via `pyvidplayer2`
- Détection automatique des modules manquants
- Installation automatique des dépendances système (`portaudio`, etc.)

## Dépendances

### Python (via `requirements.txt`)
- `pygame`
- `pyvidplayer2`
- `imageio[ffmpeg,pyav]`

### Système
- `portaudio` (nécessaire pour certaines bibliothèques audio)
- `ffmpeg` (à installer manuellement)

## Installation

### Étape 1 – Cloner le dépôt

```bash
git clone https://github.com/Benahmed-Adam/notepad--.git
cd notepad--
```

### Étape 2 - Exécuter le script de démarrage

```bash
python start.py
```

Le script détecte automatiquement les dépendances manquantes (normalement) et :

- Propose d’installer `portaudio` si nécessaire
- Installe les paquets Python

### Étape 3 - Profiter
Profitez de l'incroyable expérience que vous fournit NotePad--

## Utilisation
Une fois `main.py` lancé (automatiquement ou manuellement), l'éditeur de texte s'ouvre. Interface et fonctionnalités sont accessibles via l'interface graphique

## Structure du projet
```
├── start.py               # Script de démarrage et d'installation
├── main.py                # Point d’entrée de l’application
├── requirements.txt       # Dépendances Python
├── resources/             # Fichiers statiques (sons, images, vidéos)
└── README.md              # Documentation
└── etc...
```

## Compatibilité système
C'est censé marcher un peu partout...

## Licence

Ce projet est distribué sous la licence GPL-3.0 license. Voir le fichier [license](LICENSE) pour plus d'informations.

## Contact

- Auteur : Benahmed Adam
- Github :  https://github.com/Benahmed-Adam