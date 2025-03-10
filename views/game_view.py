import pygame

class GameView:
    def __init__(self, controller, tile_size):
        pygame.init()
        self.controller = controller
        self.tile_size = tile_size
        self.screen = pygame.display.set_mode(
            (controller.map.width * tile_size, controller.map.height * tile_size))
        pygame.display.set_caption("Pokémon Game")

        # ✅ Charger les textures de la ville
        self.textures = {
            "P": pygame.image.load("assets/tiles/path.png").convert_alpha(),
            "H": pygame.image.load("assets/tiles/grass.png").convert_alpha(),
            "M": pygame.image.load("assets/tiles/house.png").convert_alpha(),
            "C": pygame.image.load("assets/tiles/pokecenter.png").convert_alpha(),
            "S": pygame.image.load("assets/tiles/shop.png").convert_alpha(),
            "A": pygame.image.load("assets/tiles/tree.png").convert_alpha(),
            "W": pygame.image.load("assets/tiles/water.png").convert_alpha()
        }
        for key in self.textures:
            self.textures[key] = pygame.transform.scale(self.textures[key], (tile_size, tile_size))

        # ✅ Charger les sprites de Mew
        self.sprites = {
            "down": [
                pygame.image.load("assets/sprites/mew/mew_down_frame0.png").convert_alpha(),
                pygame.image.load("assets/sprites/mew/mew_down_frame1.png").convert_alpha()
            ],
            "up": [
                pygame.image.load("assets/sprites/mew/mew_up_frame0.png").convert_alpha(),
                pygame.image.load("assets/sprites/mew/mew_up_frame1.png").convert_alpha()
            ],
            "left": [
                pygame.image.load("assets/sprites/mew/mew_left_frame0.png").convert_alpha(),
                pygame.image.load("assets/sprites/mew/mew_left_frame1.png").convert_alpha()
            ],
            "right": [
                pygame.image.load("assets/sprites/mew/mew_right_frame0.png").convert_alpha(),
                pygame.image.load("assets/sprites/mew/mew_right_frame1.png").convert_alpha()
            ]
        }

        # ✅ Redimensionner les sprites pour s’adapter à la grille
        for direction in self.sprites:
            for i in range(len(self.sprites[direction])):
                sprite = self.sprites[direction][i]
                new_width = int(self.tile_size * 0.8)
                new_height = int(new_width * (sprite.get_height() / sprite.get_width()))
                self.sprites[direction][i] = pygame.transform.scale(sprite, (new_width, new_height))

        self.current_direction = "down"
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 150
        self.is_moving = False

    def render(self):
        """ Rafraîchit l'écran et affiche la carte + Mew """
        self.screen.fill((135, 206, 235))  # Fond bleu ciel

        # ✅ Affichage de la carte avec textures
        for y, row in enumerate(self.controller.map.grid):
            for x, tile in enumerate(row):
                if tile in self.textures:
                    self.screen.blit(self.textures[tile], (x * self.tile_size, y * self.tile_size))

        # ✅ Gestion de l’animation de Mew
        if self.is_moving:
            current_time = pygame.time.get_ticks()
            if current_time - self.animation_timer > self.animation_speed:
                self.animation_timer = current_time
                self.current_frame = (self.current_frame + 1) % len(self.sprites[self.current_direction])
        else:
            self.current_frame = 0  # Mew reste statique s'il ne bouge pas

        # ✅ Affichage de Mew
        player_x = self.controller.player.position[0] * self.tile_size
        player_y = self.controller.player.position[1] * self.tile_size
        current_sprite = self.sprites[self.current_direction][self.current_frame]

        offset_x = (self.tile_size - current_sprite.get_width()) // 2
        offset_y = self.tile_size - current_sprite.get_height()

        self.screen.blit(current_sprite, (player_x + offset_x, player_y + offset_y))

        pygame.display.flip()  # ✅ Rafraîchir l’écran après chaque frame

    def update_player_sprite(self, direction):
        """ Change le sprite selon la direction de Mew et anime le mouvement """
        if direction in self.sprites:
            self.current_direction = direction
            self.is_moving = True
            self.animation_timer = pygame.time.get_ticks()

    def stop_player_animation(self):
        """ Arrête l'animation quand Mew ne bouge plus """
        self.is_moving = False
        self.current_frame = 0

