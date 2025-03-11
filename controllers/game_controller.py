import pygame
import random
import os
from models.player import Player
from models.pokemon import Pokemon
from models.inventory import Inventory
from views.game_view import GameView
from models.combat import Combat
from views.combat_view import CombatView
from views.team_view import TeamView
from utils.pokeapi import fetch_pokemon, fetch_trainer_sprite

# Importer les deux types de cartes
try:
    from utils.map_loader import TiledMap
    USE_TILED = True
except ImportError:
    USE_TILED = False
    print("⚠️ Module pytmx non trouvé. Utilisation de la carte traditionnelle.")
from models.map import Map  # Toujours importer la carte traditionnelle comme fallback

class GameController:
    def __init__(self):
        pygame.init()
        
        # Taille des tuiles en pixels
        self.tile_size = 40
        
        # Carte Tiled ou traditionnelle
        self.using_tiled = False
        try:
            if USE_TILED:
                map_path = "assets/maps/pokemon_map.tmx"
                if os.path.exists(map_path):
                    self.map = TiledMap(map_path)
                    self.using_tiled = True
                    print("✅ Carte Tiled chargée avec succès")
                    # Ajuster la taille des tuiles selon le facteur d'échelle
                    if hasattr(self.map, 'real_tile_width'):
                        self.tile_size = self.map.real_tile_width
                        print(f"✅ Taille des tuiles ajustée à {self.tile_size}px")
                else:
                    raise FileNotFoundError(f"Le fichier de carte {map_path} n'existe pas.")
        except Exception as e:
            print(f"❌ Impossible d'utiliser la carte Tiled: {e}")
            # Fallback vers la carte traditionnelle
            self.map = Map(width=20, height=10)
            print("✅ Carte traditionnelle chargée (fallback)")
        
        # Position initiale du joueur
        try:
            if self.using_tiled and hasattr(self.map, 'get_spawn_position'):
                spawn_x, spawn_y = self.map.get_spawn_position()
                print(f"✅ Position initiale du joueur (Tiled): ({spawn_x}, {spawn_y})")
            else:
                # Position au centre approximatif pour la carte traditionnelle
                spawn_x, spawn_y = 400, 300
                print(f"✅ Position initiale du joueur (traditionnelle): ({spawn_x}, {spawn_y})")
        except Exception as e:
            print(f"❌ Erreur lors de la récupération du point de départ: {e}")
            spawn_x, spawn_y = 400, 300
            
        # Initialiser le joueur avec la position de départ
        self.player = Player(name="Sacha", position=(spawn_x, spawn_y))
        self.inventory = Inventory()
        self.inventory.add_item("Pokeball", 5)
        
        # Rectangle pour les collisions
        self.player_rect = pygame.Rect(
            self.player.position[0],
            self.player.position[1],
            self.tile_size,
            self.tile_size
        )
        
        # Autres initialisations
        self.running = True
        self.clock = pygame.time.Clock()
        
        # Charger les Pokémon
        self._init_pokemon_team()
        
        # Initialiser les vues
        self.view = GameView(self, self.tile_size)
        self.team_view = TeamView(self)
        
        # Variables pour le débogage du mouvement
        self.debug_movement = True
        
        # Variables pour les rencontres Pokémon
        self.encounter_cooldown = 0  # Pour éviter des rencontres trop fréquentes
        
    def _init_pokemon_team(self):
        """Initialise l'équipe Pokémon du joueur"""
        try:
            pikachu_data = fetch_pokemon("pikachu")
            if pikachu_data:
                starter_pokemon = Pokemon(
                    name=pikachu_data["name"],
                    hp=pikachu_data["hp"],
                    max_hp=pikachu_data["hp"],
                    attack=pikachu_data["attack"],
                    defense=pikachu_data["defense"],
                    sprite_path=pikachu_data["sprite_path_front"],
                    sprite_path_back=pikachu_data["sprite_path_back"]
                )
                self.player.add_pokemon(starter_pokemon)
                print(f"✅ Pokémon dans l'équipe : {[p.name for p in self.player.pokemons]}")
            else:
                self._add_default_pokemon()
        except Exception as e:
            print(f"❌ Erreur lors de la récupération du Pokémon: {e}")
            self._add_default_pokemon()
    
    def _add_default_pokemon(self):
        """Ajoute un Pokémon par défaut à l'équipe du joueur"""
        default_pokemon = Pokemon(
            name="Pikachu",
            hp=100,
            max_hp=100,
            attack=55,
            defense=40,
            sprite_path="assets/sprites/pikachu_front.png",
            sprite_path_back="assets/sprites/pikachu_back.png"
        )
        self.player.add_pokemon(default_pokemon)
        print("⚠️ Utilisation d'un Pikachu par défaut")
    
    def run(self):
        """Boucle principale du jeu"""
        # Vitesse de déplacement en pixels par touche
        move_speed = 10
        
        last_position = self.player.position
        
        while self.running:
            # Diminuer le cooldown des rencontres
            if self.encounter_cooldown > 0:
                self.encounter_cooldown -= 1
            
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_t:
                        self.team_view.visible = not self.team_view.visible
                    elif event.key == pygame.K_d:
                        # Activer/désactiver le débogage
                        self.debug_movement = not self.debug_movement
                        print(f"🐛 Débogage {'activé' if self.debug_movement else 'désactivé'}")
                        
            # Gestion du mouvement
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            
            if keys[pygame.K_LEFT]:
                dx = -move_speed
                self.view.update_player_sprite("left")
            elif keys[pygame.K_RIGHT]:
                dx = move_speed
                self.view.update_player_sprite("right")
            elif keys[pygame.K_UP]:
                dy = -move_speed
                self.view.update_player_sprite("up")
            elif keys[pygame.K_DOWN]:
                dy = move_speed
                self.view.update_player_sprite("down")
            else:
                self.view.is_moving = False
            
            # Appliquer le déplacement si possible
            if dx != 0 or dy != 0:
                new_x = self.player.position[0] + dx
                new_y = self.player.position[1] + dy
                
                # Mise à jour du rectangle du joueur pour les collisions
                new_rect = pygame.Rect(new_x, new_y, self.tile_size, self.tile_size)
                
                # Vérifier si la position est valide selon le type de carte
                is_valid = False
                
                if self.using_tiled:
                    is_valid = self.map.is_walkable(new_x, new_y)
                else:
                    # Pour la carte traditionnelle
                    grid_x = new_x // self.tile_size
                    grid_y = new_y // self.tile_size
                    
                    # Vérifier les limites de la carte
                    valid_position = (0 <= grid_x < self.map.width and 
                                    0 <= grid_y < self.map.height)
                    
                    if valid_position:
                        is_valid = self.map.is_walkable(grid_x, grid_y)
                
                # Appliquer le déplacement si la position est valide
                if is_valid:
                    # Mettre à jour la position du joueur
                    self.player.position = (new_x, new_y)
                    
                    # Mise à jour du rectangle du joueur pour les collisions
                    self.player_rect.x = new_x
                    self.player_rect.y = new_y
                    
                    # Mettre à jour la caméra pour la carte Tiled
                    if self.using_tiled and hasattr(self.map, 'update'):
                        try:
                            # Force le rectangle du joueur à utiliser le centre
                            player_center_rect = pygame.Rect(
                                new_x - (self.tile_size // 2),
                                new_y - (self.tile_size // 2),
                                self.tile_size,
                                self.tile_size
                            )
                            
                            self.map.update(player_center_rect)
                            print(f"🎮 Mise à jour de la caméra à ({new_x}, {new_y})")
                        except Exception as e:
                            print(f"❌ Erreur lors de la mise à jour de la caméra: {e}")
                            import traceback
                            traceback.print_exc()
                    
                    # Vérifier les rencontres Pokémon dans l'herbe
                    self._check_pokemon_encounter(new_x, new_y)
                    
                    # Débogage du mouvement
                    if self.debug_movement and self.player.position != last_position:
                        print(f"Nouvelle position: {self.player.position}")
                        last_position = self.player.position
            
            # Rendu
            self.view.render()
            
            # Afficher l'équipe si nécessaire
            if self.team_view.visible:
                self.team_view.render()
            
            # Rafraîchir l'écran et limiter les FPS
            pygame.display.flip()
            self.clock.tick(60)
        
        # Nettoyage
        pygame.quit()
    
    def _check_pokemon_encounter(self, x, y):
        """Vérifie si une rencontre Pokémon doit se déclencher"""
        if self.encounter_cooldown > 0:
            return
        
        is_in_grass = False
        
        if self.using_tiled:
            is_in_grass = self.map.is_grass(x, y)
        else:
            # Pour la carte traditionnelle
            grid_x = x // self.tile_size
            grid_y = y // self.tile_size
            
            if 0 <= grid_x < self.map.width and 0 <= grid_y < self.map.height:
                is_in_grass = self.map.is_grass(grid_x, grid_y)
        
        # Déboguer si le joueur est dans l'herbe
        if is_in_grass and self.debug_movement:
            print("🌿 Joueur dans les hautes herbes!")
        
        # Chance de rencontre uniquement dans les hautes herbes
        if is_in_grass and random.random() < 0.03:  # 3% de chance par pas
            print("🌿 Rencontre dans les hautes herbes!")
            self._trigger_pokemon_encounter()
            self.encounter_cooldown = 60  # Environ 1 seconde à 60 FPS
    
    def _trigger_pokemon_encounter(self):
        """Déclenche une rencontre avec un Pokémon sauvage"""
        # Liste de Pokémon sauvages possibles
        wild_pokemon_options = [
            {"name": "rattata", "level": 5},
            {"name": "pidgey", "level": 4},
            {"name": "caterpie", "level": 3},
            {"name": "weedle", "level": 3}
        ]
        
        # Sélectionner un Pokémon au hasard
        pokemon_data = random.choice(wild_pokemon_options)
        
        try:
            # Récupérer les données du Pokémon
            fetched_pokemon = fetch_pokemon(pokemon_data["name"])
            
            if fetched_pokemon:
                level_multiplier = pokemon_data["level"] / 5  # Ajuster selon le niveau
                
                wild_pokemon = Pokemon(
                    name=fetched_pokemon["name"],
                    hp=int(fetched_pokemon["hp"] * level_multiplier),
                    max_hp=int(fetched_pokemon["hp"] * level_multiplier),
                    attack=int(fetched_pokemon["attack"] * level_multiplier),
                    defense=int(fetched_pokemon["defense"] * level_multiplier),
                    sprite_path=fetched_pokemon["sprite_path_front"]
                )
                
                print(f"Un {wild_pokemon.name} sauvage apparaît!")
                
                # Initialiser le combat
                combat = Combat(self.player.pokemons[0], wild_pokemon)
                combat_view = CombatView(self, combat)
                
                # Démarrer la boucle de combat
                self._handle_combat(combat, combat_view)
            
        except Exception as e:
            print(f"❌ Erreur lors de la rencontre Pokémon: {e}")
    
    def _handle_combat(self, combat, combat_view):
        """Gère la boucle de combat"""
        combat_running = True
        
        while combat_running and self.running:
            # Gestion des événements pendant le combat
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    combat_running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    combat_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Récupérer l'action du joueur
                    action = combat_view.get_button_click(event.pos)
                    
                    if action == "attack":
                        # Attaque du joueur
                        damage = combat.player_attack()
                        print(f"Vous infligez {damage} dégâts !")
                        combat_view.trigger_attack_animation()
                        
                        # Vérifier si le Pokémon sauvage est K.O.
                        if combat.wild_pokemon.is_fainted():
                            print("Le Pokémon sauvage est K.O. !")
                            combat_running = False
                        else:
                            # Contre-attaque du Pokémon sauvage
                            pygame.time.delay(500)
                            damage = combat.wild_attack()
                            print(f"Le Pokémon sauvage inflige {damage} dégâts !")
                            
                            # Vérifier si le Pokémon du joueur est K.O.
                            if combat.player_pokemon.is_fainted():
                                print("Votre Pokémon est K.O. !")
                                combat_running = False
                    
                    elif action == "run":
                        # Tentative de fuite
                        if combat.player_run():
                            print("Vous avez fui !")
                            combat_running = False
                        else:
                            print("Fuite échouée !")
                            # Attaque du Pokémon sauvage
                            damage = combat.wild_attack()
                            print(f"Le Pokémon sauvage inflige {damage} dégâts !")
                            
                            if combat.player_pokemon.is_fainted():
                                print("Votre Pokémon est K.O. !")
                                combat_running = False
                    
                    elif action == "capture":
                        # Tentative de capture
                        success = combat.attempt_capture(self.inventory)
                        
                        if success:
                            # Ajout à l'équipe si possible
                            added = self.player.add_pokemon(combat.wild_pokemon)
                            
                            if added:
                                print(f"Bravo ! {combat.wild_pokemon.name} capturé !")
                            else:
                                print("Équipe pleine, capture impossible !")
                            
                            combat_running = False
                        else:
                            print("Capture échouée !")
                            # Attaque du Pokémon sauvage
                            damage = combat.wild_attack()
                            print(f"Le Pokémon sauvage inflige {damage} dégâts !")
                            
                            if combat.player_pokemon.is_fainted():
                                print("Votre Pokémon est K.O. !")
                                combat_running = False
            
            # Rendu de l'écran de combat
            combat_view.render()
            
            # Limitation FPS
            self.clock.tick(30)









