🎮 Pygame Pokémon Adventure
Afficher l'image

Un clone de Pokémon développé avec Pygame et Python


📝 Description
Bienvenue dans cette aventure Pokémon créée avec Pygame !
Ce projet est un clone du célèbre jeu Pokémon, développé entièrement en Python.
Explore le monde, rencontre des Pokémon sauvages, combats et capture-les pour devenir le meilleur dresseur !
Afficher l'image

✨ Fonctionnalités
🗺️ Système de carte - Support de cartes Tiled et traditionnelles
⚔️ Combats au tour par tour - Affronte des Pokémon sauvages
🏆 Système de capture - Capture les Pokémon avec des Pokéballs
📊 Statistiques - HP, attaque, défense pour chaque Pokémon
🌿 Rencontres aléatoires - Dans les hautes herbes
🎒 Inventaire - Gestion des objets comme les Pokéballs et potions
🔄 Animations - Sprites animés pour les personnages et Pokémon
🔌 PokéAPI - Intégration avec l'API pour les données des Pokémon

🚀 Installation
Prérequis

Python 3.6+
pip (gestionnaire de paquets Python)

Étapes d'installation
bashCopier# 1. Clone du dépôt
git clone https://github.com/soniadevpro/pygame-pokemon.git
cd pygame-pokemon

# 2. Installation des dépendances
pip install pygame pytmx pyscroll requests

# 3. Lancement du jeu
python main.py

🎮 Comment jouer
Contrôles
Flèches directionnelles : Déplacement du personnage
T : Afficher l'équipe de Pokémon
D : Activer/désactiver le mode débogage
ESC : Quitter le jeu
Pendant les combats
Attaque : Attaquer le Pokémon adverse
Capture : Essayer de capturer le Pokémon
Fuite : Tenter de fuir le combat

🗂️ Structure du projet
Fichiers racine

extract_sprites.py - Utilitaire pour extraire les sprites
extract_tiles.py - Utilitaire pour extraire les tuiles
main.py - Point d'entrée du jeu

Dossiers principaux
📁 assets/ - Ressources du jeu

maps/ - Cartes du jeu
sprites/ - Sprites des Pokémon
tiles/ - Tuiles pour les cartes

📁 controllers/ - Contrôleurs du jeu (MVC)

game_controller.py - Contrôleur principal

📁 models/ - Modèles de données (MVC)

combat.py - Système de combat
inventory.py - Gestion de l'inventaire
map.py - Carte traditionnelle
player.py - Gestion du joueur
pokemon.py - Classe Pokémon

📁 utils/ - Utilitaires divers

map_loader.py - Chargeur de cartes Tiled
pokeapi.py - Interface avec PokéAPI
settings.py - Paramètres du jeu

📁 views/ - Interface utilisateur (MVC)

combat_view.py - Affichage des combats
game_view.py - Affichage principal du jeu
inventory_view.py - Affichage de l'inventaire
team_view.py - Affichage de l'équipe Pokémon

🛠️ Développement
Extraire des sprites
bashCopierpython extract_sprites.py
Extraire des tuiles
bashCopierpython extract_tiles.py
Ajouter un nouveau Pokémon

Utilisez l'API PokéAPI via la fonction fetch_pokemon dans utils/pokeapi.py
Ajoutez-le à la liste des Pokémon sauvages dans game_controller.py

Personnalisation des cartes
Le jeu supporte deux types de cartes :

Cartes Tiled (.tmx) : Créées avec l'éditeur Tiled
Cartes traditionnelles : Définies dans models/map.py

Afficher l'image

🤝 Contribuer
Les contributions sont les bienvenues ! Pour contribuer :

Forkez ce dépôt
Créez une branche pour votre fonctionnalité
Committez vos changements
Pushez sur la branche
Ouvrez une Pull Request


📜 Licence
Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.

🙏 Remerciements

Pygame pour le moteur de jeu
PokéAPI pour les données sur les Pokémon
Tiled pour l'éditeur de cartes
Tous les contributeurs de sprites et tilesets Pokémon


Fait avec ❤️ par SoniaDevPro
