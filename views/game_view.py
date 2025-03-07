# views/game_view.py
import pygame

class GameView:
    def __init__(self, controller, tile_size):
        pygame.init()
        self.controller = controller
        self.tile_size = tile_size
        self.screen = pygame.display.set_mode(
            (controller.map.width * tile_size, controller.map.height * tile_size))
        pygame.display.set_caption("Pokémon Game")

        self.player_x = controller.player.position[0] * tile_size
        self.player_y = controller.player.position[1] * tile_size

    def render(self):
        self.screen.fill((255, 255, 255))

        # Carte (herbes hautes en vert)
        for y, row in enumerate(self.controller.map.grid):
            for x, tile in enumerate(row):
                if tile == "G":
                    pygame.draw.rect(self.screen, (0, 255, 0),
                                     (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))

        # Joueur (rectangle bleu)
        pygame.draw.rect(
            self.screen,
            (0, 128, 255),
            (self.controller.player.position[0] * self.tile_size,
             self.controller.player.position[1] * self.tile_size,
             self.tile_size, self.tile_size)
        )

        pygame.display.flip()

    def update_player_position(self, x, y):
        pass  # Pour le moment, tu peux ignorer ou simplement garder vide.


