import pygame

class GameView:
    def __init__(self, controller, tile_size):
        pygame.init()
        self.controller = controller
        self.tile_size = tile_size
        self.screen = pygame.display.set_mode(
            (controller.map.width * tile_size, controller.map.height * tile_size))
        pygame.display.set_caption("Pokémon Game")

        # Charger les sprites individuels
        self.sprites = {
            "down": [
                pygame.image.load("assets/sprites/walk_down_static.png").convert_alpha(),
                pygame.image.load("assets/sprites/walk_down_frame1.png").convert_alpha(),
                pygame.image.load("assets/sprites/walk_down_frame2.png").convert_alpha()
            ],
            "up": [
                pygame.image.load("assets/sprites/walk_up_static.png").convert_alpha(),
                pygame.image.load("assets/sprites/walk_up_frame1.png").convert_alpha(),
                pygame.image.load("assets/sprites/walk_up_frame2.png").convert_alpha()
            ],
            "left": [
                pygame.image.load("assets/sprites/walk_left_static.png").convert_alpha(),
                pygame.image.load("assets/sprites/walk_left_frame1.png").convert_alpha(),
                pygame.image.load("assets/sprites/walk_left_frame2.png").convert_alpha()
            ],
            "right": [
                pygame.image.load("assets/sprites/walk_right_static.png").convert_alpha(),
                pygame.image.load("assets/sprites/walk_right_frame1.png").convert_alpha(),
                pygame.image.load("assets/sprites/walk_right_frame2.png").convert_alpha()
            ]
        }

        # Redimensionner les sprites
        for direction in self.sprites:
            for i in range(len(self.sprites[direction])):
                sprite = self.sprites[direction][i]
                new_width = int(self.tile_size * 0.8)
                new_height = int(new_width * (sprite.get_height() / sprite.get_width()))
                self.sprites[direction][i] = pygame.transform.scale(sprite, (new_width, new_height))

        self.current_direction = "down"  # Direction initiale
        self.current_frame = 0  # Frame initiale
        self.animation_timer = 0  # Timer pour l'animation
        self.animation_speed = 150  # Vitesse d'animation en millisecondes
        self.is_moving = False  # État de mouvement

    def load_sprites(self):
        """
        Charge les sprites individuels depuis des fichiers séparés
        """
        sprite_positions = {
            "down": [
                "assets/sprites/walk_down_static.png",
                "assets/sprites/walk_down_frame1.png", 
                "assets/sprites/walk_down_frame2.png"
            ],
            "up": [
                "assets/sprites/walk_up_static.png",
                "assets/sprites/walk_up_frame1.png", 
                "assets/sprites/walk_up_frame2.png"
            ],
            "left": [
                "assets/sprites/walk_left_static.png",
                "assets/sprites/walk_left_frame1.png", 
                "assets/sprites/walk_left_frame2.png"
            ],
            "right": [
                "assets/sprites/walk_right_static.png",
                "assets/sprites/walk_right_frame1.png", 
                "assets/sprites/walk_right_frame2.png"
            ]
        }
        
        sprites = {}
        for direction, image_paths in sprite_positions.items():
            sprites[direction] = []
            for path in image_paths:
                try:
                    # Charger l'image
                    sprite_surface = pygame.image.load(path).convert_alpha()
                    
                    # Redimensionner le sprite
                    new_width = int(self.tile_size * 0.8)
                    new_height = int(new_width * (sprite_surface.get_height() / sprite_surface.get_width()))
                    scaled_sprite = pygame.transform.scale(sprite_surface, (new_width, new_height))
                    
                    sprites[direction].append(scaled_sprite)
                    
                except pygame.error as e:
                    print(f"Erreur lors du chargement du sprite {path}: {e}")
                    # Sprite de remplacement en cas d'erreur
                    error_sprite = pygame.Surface((new_width, new_height), pygame.SRCALPHA)
                    error_sprite.fill((255, 0, 0, 128))  # Rouge semi-transparent
                    sprites[direction].append(error_sprite)
        
        return sprites

    def render(self):
        """ Rafraîchit l'écran et affiche le joueur avec son sprite """
        self.screen.fill((135, 206, 235))  # Fond bleu ciel pour le jeu

        # Dessiner la carte
        for y, row in enumerate(self.controller.map.grid):
            for x, tile in enumerate(row):
                if tile == "G":
                    pygame.draw.rect(
                        self.screen, (0, 255, 0),
                        (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))

        # Mettre à jour l'animation si le joueur est en mouvement
        if self.is_moving:
            current_time = pygame.time.get_ticks()
            if current_time - self.animation_timer > self.animation_speed:
                self.animation_timer = current_time
                self.current_frame = (self.current_frame + 1) % len(self.sprites[self.current_direction])
        else:
            # Si le joueur est statique, utiliser la frame 0 (statique)
            self.current_frame = 0

        # Obtenir le sprite actuel et vérifier qu'il existe
        if self.current_direction in self.sprites and len(self.sprites[self.current_direction]) > self.current_frame:
            current_sprite = self.sprites[self.current_direction][self.current_frame]
            
            # Obtenir la position du joueur à partir du tuple position
            player_x = self.controller.player.position[0] * self.tile_size
            player_y = self.controller.player.position[1] * self.tile_size
            
            # Obtenir les dimensions du sprite pour le centrage
            sprite_width = current_sprite.get_width()
            sprite_height = current_sprite.get_height()
            
            # CORRIGÉ: Centrage amélioré pour que le personnage soit au centre de la tuile
            # et non pas en bas à droite
            offset_x = (self.tile_size - sprite_width) // 2
            offset_y = self.tile_size - sprite_height  # Aligner sur le bas de la tuile (plus réaliste)
            
            # Afficher le sprite du joueur avec les bons décalages
            self.screen.blit(current_sprite, (player_x + offset_x, player_y + offset_y))
            
            # Mode débogage pour visualiser les limites de la tuile
            debug_mode = True  # Activé temporairement pour aider au débogage
            if debug_mode:
                # Dessiner un rectangle autour de la tuile
                pygame.draw.rect(
                    self.screen, (255, 0, 0),
                    (player_x, player_y, self.tile_size, self.tile_size),
                    1  # Épaisseur du contour
                )
                # Dessiner un point au centre de la tuile
                pygame.draw.circle(
                    self.screen, (0, 0, 255),
                    (player_x + self.tile_size // 2, player_y + self.tile_size // 2),
                    3  # Rayon du cercle
                )
        else:
            print(f"ERREUR: Sprite non disponible pour direction={self.current_direction}, frame={self.current_frame}")

    def update_player_sprite(self, direction):
        """ Change le sprite selon la direction du joueur et anime les mouvements """
        # Vérifier que la direction est valide
        if direction in self.sprites:
            self.current_direction = direction
            
            # Indiquer que le joueur est en mouvement
            self.is_moving = True
            
            # Réinitialiser le timer d'animation si on commence à bouger
            self.animation_timer = pygame.time.get_ticks()
            print(f"Direction changée à {direction}")
        else:
            print(f"ERREUR: Direction {direction} invalide. Directions disponibles: {list(self.sprites.keys())}")

    def stop_player_animation(self):
        """ Arrête l'animation quand le joueur ne bouge plus """
        self.is_moving = False
        self.current_frame = 0  # Revenir à la frame statique