🎮 Pygame Pokémon - Un clone de Pokémon en Python
Afficher l'image
📝 Description
Bienvenue dans cette aventure Pokémon créée avec Pygame ! Ce projet est un clone du célèbre jeu Pokémon, développé entièrement en Python. Explorez le monde, rencontrez des Pokémon sauvages, combattez et capturez-les !
✨ Fonctionnalités

🗺️ Exploration de carte (support des cartes Tiled et traditionnelles)
⚔️ Système de combat tour par tour
🏆 Capture de Pokémon
📊 Statistiques des Pokémon (HP, attaque, défense)
🌿 Rencontres aléatoires dans les hautes herbes
🎒 Inventaire d'objets (Pokéballs, potions)
🔄 Animations des sprites
🔌 Intégration avec l'API PokéAPI pour récupérer les données des Pokémon

🖼️ Captures d'écran
Afficher l'image
Afficher l'image
🚀 Installation
Prérequis

Python 3.6+
pip (gestionnaire de paquets Python)

Dépendances
bashCopierpip install pygame
pip install pytmx
pip install pyscroll
pip install requests
Installation

Clonez ce dépôt

bashCopiergit clone https://github.com/yourusername/soniadevpro-pygame-pokemon.git
cd soniadevpro-pygame-pokemon

Installez les dépendances

bashCopierpip install -r requirements.txt

Lancez le jeu

bashCopierpython main.py
🎮 Comment jouer

Flèches directionnelles : Déplacement du personnage
T : Afficher l'équipe de Pokémon
D : Activer/désactiver le mode débogage
ESC : Quitter le jeu

Pendant les combats :

Cliquez sur Attaque pour attaquer
Cliquez sur Capture pour essayer de capturer le Pokémon
Cliquez sur Fuite pour tenter de fuir

🗂️ Structure du projet
Copiersoniadevpro-pygame-pokemon/
├── extract_sprites.py       # Utilitaire pour extraire les sprites
├── extract_tiles.py         # Utilitaire pour extraire les tuiles
├── main.py                  # Point d'entrée du jeu
├── assets/                  # Ressources du jeu
│   ├── maps/                # Cartes du jeu
│   ├── sprites/             # Sprites des Pokémon et personnages
│   └── tiles/               # Tuiles pour les cartes
├── controllers/             # Contrôleurs du jeu
│   └── game_controller.py   # Contrôleur principal
├── models/                  # Modèles de données
│   ├── combat.py            # Système de combat
│   ├── inventory.py         # Gestion de l'inventaire
│   ├── map.py               # Carte traditionnelle
│   ├── player.py            # Gestion du joueur
│   └── pokemon.py           # Classe Pokémon
├── utils/                   # Utilitaires divers
│   ├── map_loader.py        # Chargeur de cartes Tiled
│   ├── pokeapi.py           # Interface avec PokéAPI
│   └── settings.py          # Paramètres du jeu
└── views/                   # Interface utilisateur
    ├── combat_view.py       # Affichage des combats
    ├── game_view.py         # Affichage principal du jeu
    ├── inventory_view.py    # Affichage de l'inventaire
    └── team_view.py         # Affichage de l'équipe Pokémon
🛠️ Développement
Extraire des sprites
Pour extraire les sprites d'un Pokémon depuis une spritesheet :
bashCopierpython extract_sprites.py
Extraire des tuiles
Pour extraire les tuiles depuis une tileset :
bashCopierpython extract_tiles.py
Ajouter un nouveau Pokémon

Utilisez l'API PokéAPI via la fonction fetch_pokemon dans utils/pokeapi.py
Ajoutez-le à la liste des Pokémon sauvages dans game_controller.py

🔧 Personnalisation
Cartes
Le jeu supporte deux types de cartes :

Cartes Tiled (.tmx) : Créées avec l'éditeur Tiled
Cartes traditionnelles : Définies dans models/map.py

Pour créer une nouvelle carte avec Tiled :

Installez Tiled Map Editor
Créez une nouvelle carte
Exportez au format TMX dans le dossier assets/maps/
Modifiez le chemin dans controllers/game_controller.py

🤝 Contribuer
Les contributions sont bienvenues ! N'hésitez pas à :

Fork ce dépôt
Créer une branche pour votre fonctionnalité (git checkout -b feature/amazing-feature)
Commit vos changements (git commit -m 'Add some amazing feature')
Push sur la branche (git push origin feature/amazing-feature)
Ouvrir une Pull Request

📜 Licence
Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.
🙏 Remerciements

Pygame pour le moteur de jeu
PokéAPI pour les données sur les Pokémon
Tiled pour l'éditeur de cartes
Tous les contributeurs de sprites et tilesets Pokémon


Fait avec ❤️ par SoniaDevPro
