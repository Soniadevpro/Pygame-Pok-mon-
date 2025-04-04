<div align="center">
🎮 Pygame Pokémon Adventure
<img src="https://via.placeholder.com/800x200?text=Pok%C3%A9mon+Pygame+Adventure" alt="Bannière du jeu" width="600"/>
Un clone de Pokémon développé avec Pygame et Python
Afficher l'image
Afficher l'image
Afficher l'image
Description •
Fonctionnalités •
Installation •
Comment jouer •
Structure •
Développement
</div>

📝 Description
Bienvenue dans cette aventure Pokémon créée avec Pygame ! Ce projet est un clone du célèbre jeu Pokémon, développé entièrement en Python. Explore le monde, rencontre des Pokémon sauvages, combats et capture-les pour devenir le meilleur dresseur !
<div align="center">
<table>
<tr>
<td width="50%">
<img src="https://via.placeholder.com/400x300?text=Exploration" alt="Exploration"/>
<p align="center"><em>Exploration du monde</em></p>
</td>
<td width="50%">
<img src="https://via.placeholder.com/400x300?text=Combat" alt="Combat"/>
<p align="center"><em>Système de combat</em></p>
</td>
</tr>
</table>
</div>
✨ Fonctionnalités
<table>
  <tr>
    <td>
      <ul>
        <li>🗺️ <b>Système de carte</b> - Support de cartes Tiled et traditionnelles</li>
        <li>⚔️ <b>Combats au tour par tour</b> - Affronte des Pokémon sauvages</li>
        <li>🏆 <b>Système de capture</b> - Capture les Pokémon avec des Pokéballs</li>
        <li>📊 <b>Statistiques</b> - HP, attaque, défense pour chaque Pokémon</li>
      </ul>
    </td>
    <td>
      <ul>
        <li>🌿 <b>Rencontres aléatoires</b> - Dans les hautes herbes</li>
        <li>🎒 <b>Inventaire</b> - Gestion des objets comme les Pokéballs et potions</li>
        <li>🔄 <b>Animations</b> - Sprites animés pour les personnages et Pokémon</li>
        <li>🔌 <b>PokéAPI</b> - Intégration avec l'API pour les données des Pokémon</li>
      </ul>
    </td>
  </tr>
</table>
🚀 Installation
Prérequis

Python 3.6+
pip (gestionnaire de paquets Python)

Installation en 3 étapes
bashCopier# 1. Clone du dépôt
git clone https://github.com/soniadevpro/pygame-pokemon.git
cd pygame-pokemon

# 2. Installation des dépendances
pip install pygame pytmx pyscroll requests

# 3. Lancement du jeu
python main.py
<details>
<summary><b>🔧 Problèmes courants</b></summary>

Erreur "No module named 'pygame'" : Assurez-vous d'avoir installé Pygame avec pip install pygame
Erreur "No video device" : Pygame a besoin d'un environnement graphique
Problèmes de performances : Essayez de réduire la taille de la fenêtre dans views/game_view.py

</details>
🎮 Comment jouer
<div align="center">
ToucheAction↑↓←→Déplacement du personnageTAfficher l'équipe de PokémonDActiver/désactiver le mode débogageESCQuitter le jeu
</div>
Pendant les combats

Cliquez sur Attaque pour attaquer le Pokémon adverse
Cliquez sur Capture pour essayer de capturer le Pokémon
Cliquez sur Fuite pour tenter de fuir le combat

🗂️ Structure du projet
Copiersoniadevpro-pygame-pokemon/
├── 📜 extract_sprites.py     # Utilitaire pour extraire les sprites
├── 📜 extract_tiles.py       # Utilitaire pour extraire les tuiles
├── 📜 main.py                # Point d'entrée du jeu
│
├── 📁 assets/                # Ressources du jeu
│   ├── 📁 maps/              # Cartes du jeu
│   ├── 📁 sprites/           # Sprites des Pokémon et personnages
│   └── 📁 tiles/             # Tuiles pour les cartes
│
├── 📁 controllers/           # Contrôleurs du jeu (MVC)
│   └── 📜 game_controller.py # Contrôleur principal
│
├── 📁 models/                # Modèles de données (MVC)
│   ├── 📜 combat.py          # Système de combat
│   ├── 📜 inventory.py       # Gestion de l'inventaire
│   ├── 📜 map.py             # Carte traditionnelle
│   ├── 📜 player.py          # Gestion du joueur
│   └── 📜 pokemon.py         # Classe Pokémon
│
├── 📁 utils/                 # Utilitaires divers
│   ├── 📜 map_loader.py      # Chargeur de cartes Tiled
│   ├── 📜 pokeapi.py         # Interface avec PokéAPI
│   └── 📜 settings.py        # Paramètres du jeu
│
└── 📁 views/                 # Interface utilisateur (MVC)
    ├── 📜 combat_view.py     # Affichage des combats
    ├── 📜 game_view.py       # Affichage principal du jeu
    ├── 📜 inventory_view.py  # Affichage de l'inventaire
    └── 📜 team_view.py       # Affichage de l'équipe Pokémon
🛠️ Développement
<details>
<summary><b>Extraire des sprites</b></summary>
Pour extraire les sprites d'un Pokémon depuis une spritesheet :
bashCopierpython extract_sprites.py
Cela lira le fichier assets/sprites/mew-sprite.png et extraira les sprites individuels dans assets/sprites/mew/.
</details>
<details>
<summary><b>Extraire des tuiles</b></summary>
Pour extraire les tuiles depuis un tileset :
bashCopierpython extract_tiles.py
Cela lira le fichier assets/tiles/pokemon_tiles.png et extraira les tuiles individuelles dans assets/tiles/.
</details>
<details>
<summary><b>Ajouter un nouveau Pokémon</b></summary>

Utilisez l'API PokéAPI via la fonction fetch_pokemon dans utils/pokeapi.py
Ajoutez-le à la liste des Pokémon sauvages dans game_controller.py :

pythonCopierwild_pokemon_options = [
    {"name": "rattata", "level": 5},
    {"name": "pidgey", "level": 4},
    # Ajoutez votre nouveau Pokémon ici
    {"name": "eevee", "level": 5},
]
</details>
Personnalisation des cartes
Le jeu supporte deux types de cartes :

Cartes Tiled (.tmx) : Créées avec l'éditeur Tiled
Cartes traditionnelles : Définies dans models/map.py

<div align="center">
<img src="https://via.placeholder.com/700x300?text=Exemple+de+carte+Tiled" alt="Exemple de carte Tiled" width="500"/>
<p><em>Exemple de carte créée avec Tiled Map Editor</em></p>
</div>
🤝 Contribuer
Les contributions sont les bienvenues ! Pour contribuer :

Forkez ce dépôt
Créez une branche pour votre fonctionnalité (git checkout -b feature/amazing-feature)
Committez vos changements (git commit -m 'Add some amazing feature')
Pushez sur la branche (git push origin feature/amazing-feature)
Ouvrez une Pull Request

📜 Licence
Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.
🙏 Remerciements

Pygame pour le moteur de jeu
PokéAPI pour les données sur les Pokémon
Tiled pour l'éditeur de cartes
Tous les contributeurs de sprites et tilesets Pokémon


<div align="center">
Fait avec ❤️ par SoniaDevPro
<img src="https://via.placeholder.com/150x150?text=Pikachu" alt="Pikachu" width="100"/>
</div>
