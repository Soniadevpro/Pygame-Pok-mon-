import pygame

class GameView:
    def __init__(self, controller, tile_size):
        pygame.init()
        self.controller = controller
        self.tile_size = tile_size
        self.screen = pygame.display.set_mode(
            (controller.map.width * tile_size, controller.map.height * tile_size))
        pygame.display.set_caption("Pokémon Game")

        # Charger le sprite sheet du dresseur
        self.sprite_sheet = pygame.image.load("assets/sprites/trainer_sheet.png").convert()
        
        # Obtenir la couleur exacte du fond (en utilisant le pixel en haut à gauche)
        self.blue_background = self.sprite_sheet.get_at((0, 0))
        self.sprite_sheet.set_colorkey(self.blue_background)
        
        # Découper les sprites du personnage
        self.sprites = self.load_sprites(self.sprite_sheet)
        self.current_direction = "down"  # Direction initiale
        self.current_frame = 0  # Frame initiale
        self.animation_timer = 0  # Timer pour l'animation
        self.animation_speed = 150  # Vitesse d'animation en millisecondes
        self.is_moving = False  # État de mouvement

    def load_sprites(self, sprite_sheet):
        """
        Découpe la sprite sheet de Brendan en se concentrant sur les animations de marche.
        """
        # Taille d'un sprite individuel
        sprite_width = 16
        sprite_height = 20
        
        # IMPORTANT: Voici les positions CORRIGÉES pour les animations de marche
        # Ces positions sont ajustées en fonction de l'image que vous avez partagée
        sprite_positions = {
            "down": [
                [0, 0, sprite_width, sprite_height],           # Statique face
                [sprite_width, 0, sprite_width, sprite_height], # Pas 1 face
                [sprite_width * 2, 0, sprite_width, sprite_height], # Pas 2 face
            ],
            "up": [
                [0, sprite_height, sprite_width, sprite_height],      # Statique dos
                [sprite_width, sprite_height, sprite_width, sprite_height],  # Pas 1 dos
                [sprite_width * 2, sprite_height, sprite_width, sprite_height], # Pas 2 dos
            ],
            "left": [
                [0, sprite_height * 2, sprite_width, sprite_height],      # Statique gauche
                [sprite_width, sprite_height * 2, sprite_width, sprite_height],  # Pas 1 gauche
                [sprite_width * 2, sprite_height * 2, sprite_width, sprite_height], # Pas 2 gauche
            ],
            "right": [
                [0, sprite_height * 3, sprite_width, sprite_height],      # Statique droite
                [sprite_width, sprite_height * 3, sprite_width, sprite_height],  # Pas 1 droite
                [sprite_width * 2, sprite_height * 3, sprite_width, sprite_height], # Pas 2 droite
            ],
        }
        
        # Charger les sprites avec des paramètres de débogage
        sprites = {}
        for direction, positions in sprite_positions.items():
            sprites[direction] = []
            for pos in positions:
                try:
                    # Afficher les coordonnées pour le débogage
                    print(f"Chargement du sprite {direction} à la position {pos}")
                    
                    # Extraire le sprite de la sprite sheet
                    sprite = sprite_sheet.subsurface((pos[0], pos[1], pos[2], pos[3])).copy()
                    
                    # Appliquer la transparence
                    sprite.set_colorkey(self.blue_background)
                    
                    # Créer une nouvelle surface avec canal alpha pour une meilleure transparence
                    alpha_sprite = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
                    
                    # Remplacer les pixels bleus par des pixels transparents
                    for x in range(sprite_width):
                        for y in range(sprite_height):
                            try:
                                pixel_color = sprite.get_at((x, y))
                                if pixel_color != self.blue_background:  # Si ce n'est pas le fond bleu
                                    alpha_sprite.set_at((x, y), pixel_color)
                            except IndexError:
                                continue
                    
                    # Utiliser des dimensions fixes pour conserver les proportions
                    # et s'assurer que le sprite est correctement positionné
                    new_width = int(self.tile_size * 0.8)  # 80% de la taille de la tuile
                    new_height = int(new_width * (sprite_height / sprite_width))  # Conserver le ratio
                    
                    scaled_sprite = pygame.transform.scale(alpha_sprite, (new_width, new_height))
                    sprites[direction].append(scaled_sprite)
                    
                except (ValueError, pygame.error) as e:
                    print(f"ERREUR lors du chargement du sprite {direction}, position {pos}: {e}")
                    # Créer un sprite d'erreur (rouge) pour identifier visuellement les problèmes
                    error_sprite = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
                    error_sprite.fill((255, 0, 0, 128))  # Rouge semi-transparent
                    scaled_error = pygame.transform.scale(error_sprite, (self.tile_size, self.tile_size))
                    sprites[direction].append(scaled_error)
        
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