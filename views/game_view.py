import pygame

class GameView:
    def __init__(self, controller, tile_size):
        pygame.init()
        self.controller = controller
        self.tile_size = tile_size
        self.screen = pygame.display.set_mode((
            self.controller.map.width * tile_size, 
            self.controller.map.height * tile_size))
        pygame.display.set_caption("Pokémon Game")

        # Position initiale du joueur (en pixels)
        self.player_x = self.controller.player.position[0] * self.tile_size
        self.player_y = self.controller.player.position[1] * self.tile_size

    def render(self):
        # Affichage du fond blanc
        self.screen.fill((255, 255, 255))

        # Affiche la carte (herbes hautes)
        for y, row in enumerate(self.controller.map.grid):
            for x, tile in enumerate(row):
                if tile == "G":
                    pygame.draw.rect(self.screen, (0, 255, 0), 
                        (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))

        # Affichage du joueur (rectangle bleu)
        pygame.draw.rect(
            self.screen,
            (0, 128, 255),
            (self.player_x, self.player_y, self.tile_size, self.tile_size)
        )

        pygame.display.flip()

    def update_player_position(self, x, y):
        # Transforme position (en cases) en pixels
        self.player_x = x * self.tile_size
        self.player_y = y * self.tile_size

