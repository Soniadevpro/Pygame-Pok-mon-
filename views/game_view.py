import pygame

class GameView:
    def __init__(self, controller, tile_size):
        pygame.init()
        self.controller = controller
        self.tile_size = tile_size
        
        # Dimensions de l'écran basées sur la taille de la carte
        screen_width = controller.map.width * tile_size
        screen_height = controller.map.height * tile_size
        
        # Création de l'écran avec les dimensions correctes
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Pokémon Game")

        # Initialiser le dictionnaire de textures d'abord
        self.textures = {}
        
        # Définir les chemins des fichiers de texture
        texture_paths = {
            "P": "assets/tiles/bat/pont.png",
            "H": "assets/tiles/sols/herbe.png",  # Chemin corrigé pour l'herbe
            "M": "assets/tiles/bat/ponton.png",
            "C": "assets/tiles/bat/pokecenter.png",
            "S": "assets/tiles/bat/pokeshop.png",
            "A": "assets/tiles/arbres/arbre.png",
            "W": "assets/tiles/sols/eau.png"
        }
        
        # Créer une texture par défaut pour les textures manquantes
        missing_texture = pygame.Surface((tile_size, tile_size))
        missing_texture.fill((255, 0, 255))  # Rose vif pour repérer facilement
        
        # Charger chaque texture individuellement pour gérer les erreurs
        for key, path in texture_paths.items():
            try:
                self.textures[key] = pygame.image.load(path).convert_alpha()
                print(f"✅ Texture '{key}' chargée: {path}")
            except FileNotFoundError:
                self.textures[key] = missing_texture
                print(f"⚠️ Texture '{key}' introuvable: {path}")
        
        # Redimensionner chaque texture pour qu'elle occupe exactement une tuile
        for key in self.textures:
            self.textures[key] = pygame.transform.scale(self.textures[key], (tile_size, tile_size))

        # Initialiser le dictionnaire des sprites
        self.sprites = {}
        
        # Définir les chemins des fichiers de sprites
        sprite_paths = {
            "down": [
                "assets/sprites/mew/mew_down_frame0.png",
                "assets/sprites/mew/mew_down_frame1.png"
            ],
            "up": [
                "assets/sprites/mew/mew_up_frame0.png",
                "assets/sprites/mew/mew_up_frame1.png"
            ],
            "left": [
                "assets/sprites/mew/mew_left_frame0.png",
                "assets/sprites/mew/mew_left_frame1.png"
            ],
            "right": [
                "assets/sprites/mew/mew_right_frame0.png",
                "assets/sprites/mew/mew_right_frame1.png"
            ]
        }
        
        # Créer un sprite par défaut
        default_sprite = pygame.Surface((int(tile_size * 0.8), int(tile_size * 0.8)))
        default_sprite.fill((255, 0, 0))  # Rouge pour le joueur
        
        # Charger chaque sprite individuellement
        for direction, paths in sprite_paths.items():
            self.sprites[direction] = []
            for path in paths:
                try:
                    sprite = pygame.image.load(path).convert_alpha()
                    print(f"✅ Sprite '{direction}' chargé: {path}")
                except FileNotFoundError:
                    sprite = default_sprite
                    print(f"⚠️ Sprite '{direction}' introuvable: {path}")
                
                # Redimensionner le sprite
                new_width = int(self.tile_size * 0.8)
                new_height = int(new_width * (sprite.get_height() / sprite.get_width()))
                self.sprites[direction].append(pygame.transform.scale(sprite, (new_width, new_height)))

        self.current_direction = "down"
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 150
        self.is_moving = False

    def render(self):
        """ Rafraîchit l'écran et affiche la carte + Mew """
        self.screen.fill((0, 0, 100))  # Fond bleu foncé (au cas où l'eau ne couvre pas tout)

        # Affichage de la carte avec textures
        for y, row in enumerate(self.controller.map.grid):
            for x, tile in enumerate(row):
                if tile in self.textures:
                    # Dessiner chaque tuile à la position exacte
                    self.screen.blit(self.textures[tile], (x * self.tile_size, y * self.tile_size))
                else:
                    # Dessiner un rectangle coloré pour les tuiles inconnues
                    pygame.draw.rect(
                        self.screen, 
                        (255, 0, 255),  # Rose vif pour repérer facilement
                        (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                    )
                    # Afficher le caractère de la tuile inconnue
                    font = pygame.font.Font(None, 20)
                    text = font.render(tile, True, (255, 255, 255))
                    text_rect = text.get_rect(center=(
                        x * self.tile_size + self.tile_size // 2,
                        y * self.tile_size + self.tile_size // 2
                    ))
                    self.screen.blit(text, text_rect)

        # Gestion de l'animation de Mew
        if self.is_moving:
            current_time = pygame.time.get_ticks()
            if current_time - self.animation_timer > self.animation_speed:
                self.animation_timer = current_time
                self.current_frame = (self.current_frame + 1) % len(self.sprites[self.current_direction])
        else:
            self.current_frame = 0  # Mew reste statique s'il ne bouge pas

        # Affichage de Mew
        player_x = self.controller.player.position[0] * self.tile_size
        player_y = self.controller.player.position[1] * self.tile_size
        current_sprite = self.sprites[self.current_direction][self.current_frame]

        # Centrer le sprite sur la tuile
        offset_x = (self.tile_size - current_sprite.get_width()) // 2
        offset_y = self.tile_size - current_sprite.get_height()

        self.screen.blit(current_sprite, (player_x + offset_x, player_y + offset_y))

        # Afficher des informations de débogage si nécessaire
        font = pygame.font.Font(None, 24)
        pos_text = font.render(f"Position: {self.controller.player.position}", True, (255, 255, 255))
        self.screen.blit(pos_text, (10, 10))

        pygame.display.flip()  # Rafraîchir l'écran après chaque frame

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

