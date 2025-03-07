import pygame
import random
from models.player import Player
from models.pokemon import Pokemon
from models.inventory import Inventory
from models.map import Map
from views.game_view import GameView
from models.combat import Combat
from views.combat_view import CombatView
from views.team_view import TeamView
from utils.pokeapi import fetch_pokemon, fetch_trainer_sprite

class GameController:
    def __init__(self):
        pygame.init()
        self.tile_size = 40
        self.player = Player(name="Sacha", position=(5, 5))
        self.inventory = Inventory()
        self.map = Map(width=20, height=15)
        self.running = True
        self.clock = pygame.time.Clock()

        # Récupérer le sprite du dresseur
        trainer_sprite_path = fetch_trainer_sprite("red")
        self.trainer_sprite = pygame.image.load(trainer_sprite_path)
        self.trainer_sprite = pygame.transform.scale(self.trainer_sprite, (40, 40))
        
        # Récupérer Pikachu depuis PokéAPI
        pikachu_data = fetch_pokemon("pikachu")
        if pikachu_data:
            starter_pokemon = Pokemon(
                name=pikachu_data["name"],
                hp=pikachu_data["hp"],
                max_hp=pikachu_data["hp"],
                attack=pikachu_data["attack"],
                defense=pikachu_data["defense"],
                sprite_path=pikachu_data["sprite_path"]
            )
            self.player.add_pokemon(starter_pokemon)

        # Vérifier que Pikachu est bien ajouté
        print(f"Pokémon dans l'équipe : {[p.name for p in self.player.pokemons]}")
        
        self.view = GameView(self, self.tile_size)
        self.team_view = TeamView(self)
    
    def run(self):
        move_cooldown = 150
        last_move = pygame.time.get_ticks()
        is_key_pressed = False  # Variable pour suivre si une touche de direction est enfoncée

        while self.running:
            current_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_t:
                        self.team_view.visible = not self.team_view.visible
                    # Détection des touches de direction enfoncées
                    elif event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                        is_key_pressed = True
                elif event.type == pygame.KEYUP:
                    # Détection des touches de direction relâchées
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                        is_key_pressed = False
                        self.view.stop_player_animation()  # Arrêter l'animation quand on relâche les touches

            keys = pygame.key.get_pressed()
            dx, dy = 0, 0

            # Vérifier le mouvement
            if current_time - last_move > move_cooldown:
                if keys[pygame.K_LEFT]:
                    dx = -1
                    self.view.update_player_sprite("left")
                elif keys[pygame.K_RIGHT]:
                    dx = 1
                    self.view.update_player_sprite("right")
                elif keys[pygame.K_UP]:
                    dy = -1
                    self.view.update_player_sprite("up")
                elif keys[pygame.K_DOWN]:
                    dy = 1
                    self.view.update_player_sprite("down")
                else:
                    # Si aucune touche n'est enfoncée, arrêter l'animation
                    self.view.is_moving = False

                if dx != 0 or dy != 0:
                    new_x = self.player.position[0] + dx
                    new_y = self.player.position[1] + dy
                    if 0 <= new_x < self.map.width and 0 <= new_y < self.map.height:
                        self.player.position = (new_x, new_y)
                        self.check_for_encounter()
                    last_move = current_time

            self.view.render()
            if self.team_view.visible:
                self.team_view.render()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def check_for_encounter(self):
        x, y = self.player.position
        if self.map.grid[y][x] == "G" and random.random() < 0.1:
            wild_pokemon = Pokemon(name="Rattata", hp=30, max_hp=30, attack=30, defense=15)
            combat = Combat(self.player.pokemons[0], wild_pokemon)
            print("Un Pokémon sauvage apparaît !")

            combat_running = True
            combat_view = CombatView(self, combat)

            while combat_running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        combat_running = False

                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        action = combat_view.get_button_click(event.pos)

                        if action == "attack":
                            damage = combat.player_attack()
                            print(f"Vous infligez {damage} dégâts !")

                            if combat.wild_pokemon.is_fainted():
                                print("Pokémon sauvage KO !")
                                combat_running = False
                            else:
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
                                print("Échec de la fuite !")
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








