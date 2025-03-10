import pygame

class GameView:
    def __init__(self, controller, tile_size):
        pygame.init()
        self.controller = controller
        self.tile_size = tile_size
        
        # Dimensions de l'écran
        screen_width = 800  # Largeur fixe 
        screen_height = 600  # Hauteur fixe
        
        # Création de l'écran avec les dimensions adaptées
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Pokémon Game")

        # Initialiser le dictionnaire des sprites
        self.load_player_sprites()
        
        # Initialiser les variables d'animation
        self.current_direction = "down"
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 150
        self.is_moving = False
        
        # Polices pour le texte
        self.font = pygame.font.Font(None, 24)
        
        print("✅ Vue du jeu initialisée")
    
    def load_player_sprites(self):
        """Charge les sprites du joueur depuis les fichiers"""
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
        default_sprite = pygame.Surface((int(self.tile_size * 0.8), int(self.tile_size * 0.8)))
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
                new_height = int(self.tile_size * 0.8)  # Utilisez directement la même largeur pour un ratio 1:1
                self.sprites[direction].append(pygame.transform.scale(sprite, (new_width, new_height)))

    def render(self):
        """Rafraîchit l'écran et affiche la carte + le joueur"""
        # Effacer l'écran
        self.screen.fill((0, 0, 0))
        
        # Si nous avons une carte Tiled, utiliser sa méthode de rendu
        if hasattr(self.controller.map, 'render'):
            self.controller.map.render(self.screen)
        else:
            # Méthode alternative si nous n'utilisons pas Tiled
            self._render_fallback_map()
        
        # Gestion de l'animation du joueur
        if self.is_moving:
            current_time = pygame.time.get_ticks()
            if current_time - self.animation_timer > self.animation_speed:
                self.animation_timer = current_time
                self.current_frame = (self.current_frame + 1) % len(self.sprites[self.current_direction])
        else:
            self.current_frame = 0  # Le joueur reste statique s'il ne bouge pas

        # Affichage du joueur
        current_sprite = self.sprites[self.current_direction][self.current_frame]

        # Obtenir la position du joueur à l'écran (tenant compte du défilement)
        if hasattr(self.controller.map, 'map_layer'):
            # Si nous utilisons pyscroll, le joueur est centré
            screen_center_x = self.screen.get_width() // 2
            screen_center_y = self.screen.get_height() // 2
            
            # Centrer le sprite sur la tuile
            offset_x = (self.tile_size - current_sprite.get_width()) // 2
            offset_y = (self.tile_size - current_sprite.get_height()) // 2
            
            self.screen.blit(current_sprite, (screen_center_x - self.tile_size // 2 + offset_x, 
                                              screen_center_y - self.tile_size // 2 + offset_y))
        else:
            # Méthode alternative sans pyscroll
            player_x, player_y = self.controller.player.position
            
            # Centrer le sprite sur la tuile
            offset_x = (self.tile_size - current_sprite.get_width()) // 2
            offset_y = (self.tile_size - current_sprite.get_height()) // 2
            
            self.screen.blit(current_sprite, (player_x + offset_x, player_y + offset_y))

        # Afficher des informations de débogage
        self._render_debug_info()
        
        pygame.display.flip()  # Rafraîchir l'écran après chaque frame
    
    def _render_fallback_map(self):
        """Méthode de secours pour afficher la carte si Tiled n'est pas utilisé"""
        # Cette méthode utilise l'ancien système de rendu
        for y, row in enumerate(self.controller.map.grid):
            for x, tile in enumerate(row):
                if hasattr(self, 'textures') and tile in self.textures:
                    # Si nous avons des textures définies
                    self.screen.blit(self.textures[tile], (x * self.tile_size, y * self.tile_size))
                else:
                    # Afficher des rectangles colorés pour les différents types de tuiles
                    colors = {
                        "W": (0, 0, 255),      # Eau (bleu)
                        "G": (0, 200, 0),      # Herbe (vert)
                        "P": (150, 120, 70),   # Chemin (marron)
                        "A": (0, 100, 0),      # Arbre (vert foncé)
                        "M": (150, 150, 150),  # Ponton (gris)
                        "C": (255, 50, 50),    # Centre Pokémon (rouge)
                        "S": (50, 50, 255),    # PokéMart (bleu)
                        ".": (100, 100, 100)   # Défaut (gris)
                    }
                    
                    color = colors.get(tile, (100, 100, 100))
                    pygame.draw.rect(
                        self.screen, 
                        color, 
                        (x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                    )
                    
                    # Afficher le caractère de la tuile
                    text = self.font.render(tile, True, (255, 255, 255))
                    text_rect = text.get_rect(center=(
                        x * self.tile_size + self.tile_size // 2,
                        y * self.tile_size + self.tile_size // 2
                    ))
                    self.screen.blit(text, text_rect)
    
    def _render_debug_info(self):
        """Affiche des informations de débogage à l'écran"""
        # Afficher la position du joueur
        position_text = f"Position: ({self.controller.player.position[0]}, {self.controller.player.position[1]})"
        position_surface = self.font.render(position_text, True, (255, 255, 255))
        self.screen.blit(position_surface, (10, 10))
        
        # Afficher l'inventaire
        inventory_text = f"Inventaire: {str(self.controller.inventory)}"
        inventory_surface = self.font.render(inventory_text, True, (255, 255, 255))
        self.screen.blit(inventory_surface, (10, 40))
        
        # Afficher les FPS
        fps = int(self.controller.clock.get_fps())
        fps_text = f"FPS: {fps}"
        fps_surface = self.font.render(fps_text, True, (255, 255, 255))
        self.screen.blit(fps_surface, (10, 70))

    def update_player_sprite(self, direction):
        """Change le sprite selon la direction du joueur et anime le mouvement"""
        if direction in self.sprites:
            self.current_direction = direction
            self.is_moving = True
            self.animation_timer = pygame.time.get_ticks()

    def stop_player_animation(self):
        """Arrête l'animation quand le joueur ne bouge plus"""
        self.is_moving = False
        self.current_frame = 0

