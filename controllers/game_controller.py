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
from utils.map_loader import TiledMap  # Notre nouveau chargeur de carte

class GameController:
    def __init__(self):
        pygame.init()
        
        # Créer le dossier de cartes s'il n'existe pas
        os.makedirs("assets/maps", exist_ok=True)
        
        # Vérifier si le fichier de carte existe
        map_path = "assets/maps/pokemon_map.tmx"
        if not os.path.exists(map_path):
            print(f"⚠️ Le fichier de carte {map_path} n'existe pas. Créez-le avec Tiled.")
            print("⚠️ Utilisation d'une carte par défaut pour le moment.")
            # À ce stade, vous pourriez générer une carte par défaut ou utiliser
            # votre ancienne classe Map en attendant de créer une carte avec Tiled
        
        try:
            # Charger la carte Tiled
            self.map = TiledMap(map_path)
            self.tile_size = self.map.tile_width  # Utiliser la taille des tuiles de la carte
        except Exception as e:
            # En cas d'erreur, on pourrait revenir à l'ancienne méthode
            print(f"❌ Erreur lors du chargement de la carte Tiled: {e}")
            print("⚠️ Chargement d'une carte par défaut...")
            from models.map import Map  # Importation conditionnelle de l'ancienne Map
            self.map = Map(width=20, height=10)
            self.tile_size = 40  # Taille par défaut
        
        # Position initiale du joueur (à partir de la carte ou par défaut)
        try:
            spawn_x, spawn_y = self.map.get_spawn_position()
            print(f"Position initiale du joueur: ({spawn_x}, {spawn_y})")
        except AttributeError:
            # Si nous utilisons l'ancienne classe Map, définir une position par défaut
            spawn_x, spawn_y = 5 * self.tile_size, 5 * self.tile_size
            print(f"Position par défaut du joueur: ({spawn_x}, {spawn_y})")
        
        # Initialiser le joueur
        self.player = Player(name="Sacha", position=(spawn_x, spawn_y))
        self.inventory = Inventory()
        self.running = True
        self.clock = pygame.time.Clock()
        
        # Rectangle pour les collisions
        self.player_rect = pygame.Rect(
            self.player.position[0],
            self.player.position[1],
            self.tile_size,
            self.tile_size
        )
        
        # Initialiser le sprite du dresseur
        self._init_trainer_sprite()
        
        # Initialiser les Pokémon du joueur
        self._init_player_pokemon()
        
        # Initialiser les vues
        self.view = GameView(self, self.tile_size)
        self.team_view = TeamView(self)
    
    def _init_trainer_sprite(self):
        """Initialise le sprite du dresseur"""
        try:
            trainer_sprite_path = fetch_trainer_sprite("red")
            self.trainer_sprite = pygame.image.load(trainer_sprite_path)
            self.trainer_sprite = pygame.transform.scale(self.trainer_sprite, (self.tile_size, self.tile_size))
        except Exception as e:
            print(f"❌ Erreur lors du chargement du sprite du dresseur: {e}")
            # Créer un sprite par défaut
            self.trainer_sprite = pygame.Surface((self.tile_size, self.tile_size))
            self.trainer_sprite.fill((255, 0, 0))
    
    def _init_player_pokemon(self):
        """Initialise les Pokémon du joueur"""
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
                # Créer un Pokémon par défaut si l'API échoue
                self._add_default_pokemon()
        except Exception as e:
            print(f"❌ Erreur lors de la récupération du Pokémon: {e}")
            # Créer un Pokémon par défaut en cas d'erreur
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
        move_cooldown = 150  # Délai entre les mouvements (en millisecondes)
        last_move = pygame.time.get_ticks()
        is_key_pressed = False

        while self.running:
            current_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        self.team_view.visible = not self.team_view.visible
                    elif event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                        is_key_pressed = True
                elif event.type == pygame.KEYUP:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                        is_key_pressed = False
                        self.view.stop_player_animation()

            # Gestion du mouvement avec vérification des collisions
            if current_time - last_move > move_cooldown:
                keys = pygame.key.get_pressed()
                dx, dy = 0, 0
                move_speed = self.tile_size // 4  # Vitesse de déplacement

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

                if dx != 0 or dy != 0:
                    new_x = self.player.position[0] + dx
                    new_y = self.player.position[1] + dy
                    
                    # Vérifier si la nouvelle position est praticable
                    if hasattr(self.map, 'is_walkable') and self.map.is_walkable(new_x, new_y):
                        self.player.position = (new_x, new_y)
                        self.player_rect.x = new_x
                        self.player_rect.y = new_y
                        
                        # Mettre à jour la vue de la carte pour centrer sur le joueur
                        if hasattr(self.map, 'update'):
                            self.map.update(self.player_rect)
                        
                        # Vérifier les rencontres de Pokémon
                        if hasattr(self.map, 'is_grass') and self.map.is_grass(new_x, new_y):
                            if random.random() < 0.05:  # 5% de chance de rencontre
                                self.trigger_pokemon_encounter()
                    
                    last_move = current_time

            # Rendu de l'écran
            self.view.render()
            if self.team_view.visible:
                self.team_view.render()
            
            self.clock.tick(60)  # 60 FPS

        pygame.quit()

    def trigger_pokemon_encounter(self):
        """Déclenche une rencontre avec un Pokémon sauvage"""
        try:
            # Liste de Pokémon possibles à rencontrer (possibilité d'adapter selon la zone)
            pokemon_options = ["rattata", "pidgey", "weedle", "caterpie"]
            wild_pokemon_name = random.choice(pokemon_options)
            
            wild_pokemon_data = fetch_pokemon(wild_pokemon_name)
            if wild_pokemon_data:
                wild_pokemon = Pokemon(
                    name=wild_pokemon_data["name"],
                    hp=wild_pokemon_data["hp"],
                    max_hp=wild_pokemon_data["hp"],
                    attack=wild_pokemon_data["attack"],
                    defense=wild_pokemon_data["defense"],
                    sprite_path=wild_pokemon_data.get("sprite_path_front", "assets/sprites/default.png")
                )
                
                print(f"Un {wild_pokemon.name} sauvage apparaît!")

                combat = Combat(self.player.pokemons[0], wild_pokemon)
                combat_view = CombatView(self, combat)

                self._handle_combat(combat, combat_view)
        except Exception as e:
            print(f"❌ Erreur lors de la rencontre avec un Pokémon sauvage: {e}")
    
    def _handle_combat(self, combat, combat_view):
        """Gère le déroulement d'un combat"""
        combat_running = True
        while combat_running and self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    combat_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    action = combat_view.get_button_click(event.pos)

                    if action == "attack":
                        damage = combat.player_attack()
                        print(f"Vous infligez {damage} dégâts !")
                        combat_view.trigger_attack_animation()

                        if combat.wild_pokemon.is_fainted():
                            print("Le Pokémon sauvage est KO !")
                            combat_running = False
                        else:
                            pygame.time.delay(500)
                            damage = combat.wild_attack()
                            print(f"Le Pokémon sauvage inflige {damage} dégâts !")
                            if combat.player_pokemon.is_fainted():
                                print("Votre Pokémon est KO !")
                                combat_running = False

                    elif action == "run":
                        if combat.player_run():
                            print("Vous avez fui !")
                            combat_running = False
                        else:
                            print("Fuite échouée !")
                            damage = combat.wild_attack()
                            print(f"Le Pokémon sauvage inflige {damage} dégâts !")
                            if combat.player_pokemon.is_fainted():
                                print("Votre Pokémon est KO !")
                                combat_running = False

                    elif action == "capture":
                        success = combat.attempt_capture(self.inventory)
                        if success:
                            added = self.player.add_pokemon(combat.wild_pokemon)
                            if added:
                                print(f"Bravo ! {combat.wild_pokemon.name} capturé !")
                            else:
                                print("Équipe pleine, capture impossible !")
                            combat_running = False
                        else:
                            print("Capture échouée !")
                            damage = combat.wild_attack()
                            print(f"Le Pokémon sauvage inflige {damage} dégâts !")
                            if combat.player_pokemon.is_fainted():
                                print("Votre Pokémon est KO !")
                                combat_running = False

            combat_view.render()
            self.clock.tick(30)









