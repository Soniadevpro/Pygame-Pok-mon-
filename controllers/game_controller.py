# controllers/game_controller.py
import pygame
import random
from models.player import Player
from models.pokemon import Pokemon
from models.inventory import Inventory
from models.map import Map
from views.game_view import GameView
from models.combat import Combat
from views.combat_view import CombatView

class GameController:
    def __init__(self):
        pygame.init()
        self.tile_size = 40  # taille d'une case
        self.player = Player(name="Sacha", position=(5, 5))  # coordonnées en cases
        starter_pokemon = Pokemon(name="Pikachu", hp=35, max_hp=35, attack=55, defense=40)
        self.player.add_pokemon(starter_pokemon)
        self.inventory = Inventory()
        self.map = Map(width=20, height=15)  # plus grande carte pour avoir de l'espace
        self.view = GameView(self, self.tile_size)
        self.running = True
        self.clock = pygame.time.Clock()

    def run(self):
        move_cooldown = 150  # Temps en ms entre chaque déplacement
        last_move = pygame.time.get_ticks()

        while self.running:
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            dx, dy = 0, 0

            if current_time - last_move > move_cooldown:
                if keys[pygame.K_LEFT]:
                    dx = -1
                elif keys[pygame.K_RIGHT]:
                    dx = 1
                elif keys[pygame.K_UP]:
                    dy = -1
                elif keys[pygame.K_DOWN]:
                    dy = 1

                if dx != 0 or dy != 0:
                    new_x = self.player.position[0] + dx
                    new_y = self.player.position[1] + dy

                    # Vérifie limites de la carte avant de déplacer
                    if 0 <= new_x < self.map.width and 0 <= new_y < self.map.height:
                        self.player.position = (new_x, new_y)
                        self.view.update_player_position(new_x, new_y)
                        self.check_for_encounter()

                    last_move = current_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.view.render()
            self.clock.tick(60)

        pygame.quit()


    def check_for_encounter(self):
        x, y = self.player.position
        if self.map.grid[y][x] == "G":
            if random.random() < 0.1:
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
                            
                    combat_view.render()
                    pygame.display.flip()
                    
                    
                    if combat.is_over():
                        print("Combat terminé !")
                        combat_running = False
                        
                        
                    self.clock.tick(30)


