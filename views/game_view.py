import pygame
import random

class GameView:
    def __init__(self, controller, tile_size):
        pygame.init()
        self.controller = controller
        self.tile_size = tile_size
        
        # Dimensions de l'écran
        self.screen_width = 800
        self.screen_height = 600
        
        # Création de l'écran
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pokémon Game")
        
        # Charger les sprites du joueur
        self.sprites = self.load_player_sprites()
        
        # Créer les textures pour la carte traditionnelle (si nécessaire)
        if not self.controller.using_tiled:
            self.textures = self.create_textures()
        
        # Variables d'animation
        self.current_direction = "down"
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 150
        self.is_moving = False
        
        # Police pour les textes de débogage
        self.font = pygame.font.Font(None, 24)
        
        print(f"✅ Vue du jeu initialisée (mode {'Tiled' if self.controller.using_tiled else 'Traditionnel'})")
    
    def create_textures(self):
        """Crée des textures simples pour les différents types de tuiles (carte traditionnelle)"""
        textures = {}
        
        # Eau (bleu)
        water = pygame.Surface((self.tile_size, self.tile_size))
        water.fill((0, 0, 220))
        textures["W"] = water
        
        # Pont (marron)
        bridge = pygame.Surface((self.tile_size, self.tile_size))
        bridge.fill((150, 100, 50))
        textures["P"] = bridge
        
        # Herbe (vert)
        grass = pygame.Surface((self.tile_size, self.tile_size))
        grass.fill((0, 180, 0))
        grass_pattern = pygame.Surface((4, 4))
        grass_pattern.fill((0, 200, 0))
        for i in range(5):
            x, y = random.randint(0, self.tile_size-5), random.randint(0, self.tile_size-5)
            grass.blit(grass_pattern, (x, y))
        textures["H"] = grass
        
        # Ponton (gris)
        dock = pygame.Surface((self.tile_size, self.tile_size))
        dock.fill((150, 150, 150))
        textures["M"] = dock
        
        # Centre Pokémon (rouge)
        pokecenter = pygame.Surface((self.tile_size, self.tile_size))
        pokecenter.fill((220, 50, 50))
        textures["C"] = pokecenter
        
        # PokéMart (bleu)
        pokemart = pygame.Surface((self.tile_size, self.tile_size))
        pokemart.fill((50, 50, 220))
        textures["S"] = pokemart
        
        # Arbre (vert foncé)
        tree = pygame.Surface((self.tile_size, self.tile_size))
        tree.fill((0, 100, 0))
        textures["A"] = tree
        
        # Défaut (gris)
        default = pygame.Surface((self.tile_size, self.tile_size))
        default.fill((100, 100, 100))
        textures["."] = default
        
        return textures
    
    def load_player_sprites(self):
        """Charge les sprites du joueur"""
        sprites = {}
        
        # Chemins des sprites par direction
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
        
        # Sprite par défaut (rectangle rouge)
        default_sprite = pygame.Surface((self.tile_size, self.tile_size))
        default_sprite.fill((255, 0, 0))
        
        # Charger chaque sprite
        for direction, paths in sprite_paths.items():
            sprites[direction] = []
            for path in paths:
                try:
                    sprite = pygame.image.load(path).convert_alpha()
                    # Redimensionner au format carré
                    sprite = pygame.transform.scale(sprite, (self.tile_size, self.tile_size))
                    sprites[direction].append(sprite)
                    print(f"✅ Sprite '{direction}' chargé: {path}")
                except Exception as e:
                    sprites[direction].append(default_sprite)
                    print(f"⚠️ Erreur de chargement du sprite '{direction}': {e}")
        
        return sprites
    
    def render(self):
        """Affiche le jeu à l'écran"""
        # Effacer l'écran avec un fond uni
        self.screen.fill((0, 0, 0))  # Noir par défaut
        
        # Afficher la carte appropriée
        if self.controller.using_tiled:
            self._render_tiled_map()
        else:
            self._render_traditional_map()
        
        # Gestion de l'animation du joueur
        if self.is_moving:
            current_time = pygame.time.get_ticks()
            if current_time - self.animation_timer > self.animation_speed:
                self.animation_timer = current_time
                self.current_frame = (self.current_frame + 1) % len(self.sprites[self.current_direction])
        else:
            self.current_frame = 0
        
        # Obtenir le sprite actuel
        current_sprite = self.sprites[self.current_direction][self.current_frame]
        
        # Afficher le joueur
        if self.controller.using_tiled:
            # En mode Tiled, le joueur est toujours au centre de l'écran
            center_x = self.screen_width // 2
            center_y = self.screen_height // 2
            
            # Ajuster le positionnement du sprite
            sprite_rect = current_sprite.get_rect()
            sprite_rect.centerx = center_x
            sprite_rect.centery = center_y
            
            self.screen.blit(current_sprite, sprite_rect)
            
            # Debug: dessiner un repère pour le centre de l'écran
            pygame.draw.circle(self.screen, (255, 0, 0), (center_x, center_y), 3)
        else:
            # En mode traditionnel, le joueur est à sa position absolue
            player_x, player_y = self.controller.player.position
            self.screen.blit(current_sprite, (player_x, player_y))
        
        # Afficher les informations de débogage
        self._draw_debug_info()
    
    def _render_tiled_map(self):
        """Affiche la carte Tiled"""
        if hasattr(self.controller.map, 'render'):
            self.controller.map.render(self.screen)
        else:
            # Fallback au cas où render n'existe pas
            self.screen.fill((135, 206, 235))  # Bleu ciel
    
    def _render_traditional_map(self):
        """Dessine la carte traditionnelle en utilisant les textures"""
        # Fond bleu ciel par défaut
        self.screen.fill((135, 206, 235))
        
        map_data = self.controller.map.grid
        
        for y, row in enumerate(map_data):
            for x, tile in enumerate(row):
                # Position à l'écran
                screen_x = x * self.tile_size
                screen_y = y * self.tile_size
                
                # Obtenir la texture pour ce type de tuile
                texture = self.textures.get(tile, self.textures.get(".", None))
                
                if texture:
                    # Afficher la texture
                    self.screen.blit(texture, (screen_x, screen_y))
                else:
                    # Fallback si la texture est manquante
                    pygame.draw.rect(
                        self.screen,
                        (100, 100, 100),
                        (screen_x, screen_y, self.tile_size, self.tile_size)
                    )
                    
                    # Afficher le caractère de la tuile
                    text = self.font.render(tile, True, (255, 255, 255))
                    text_rect = text.get_rect(center=(
                        screen_x + self.tile_size // 2,
                        screen_y + self.tile_size // 2
                    ))
                    self.screen.blit(text, text_rect)
    
    def _draw_debug_info(self):
        """Affiche des informations de débogage"""
        # Position du joueur
        player_x, player_y = self.controller.player.position
        position_text = f"Position: ({player_x}, {player_y})"
        position_surface = self.font.render(position_text, True, (255, 255, 255))
        self.screen.blit(position_surface, (10, 10))
        
        # Position en tuiles
        if self.controller.using_tiled:
            tile_x = int(player_x / self.controller.map.real_tile_width)
            tile_y = int(player_y / self.controller.map.real_tile_height)
        else:
            tile_x = player_x // self.tile_size
            tile_y = player_y // self.tile_size
            
        grid_text = f"Tuile: ({tile_x}, {tile_y})"
        grid_surface = self.font.render(grid_text, True, (255, 255, 255))
        self.screen.blit(grid_surface, (10, 40))
        
        # Type de carte
        map_type = "Tiled" if self.controller.using_tiled else "Traditionnelle"
        type_text = f"Carte: {map_type}"
        type_surface = self.font.render(type_text, True, (255, 255, 255))
        self.screen.blit(type_surface, (10, 70))
        
        # FPS
        fps = int(self.controller.clock.get_fps())
        fps_text = f"FPS: {fps}"
        fps_surface = self.font.render(fps_text, True, (255, 255, 255))
        self.screen.blit(fps_surface, (10, 100))
        
        # Instruction
        help_text = "Flèches=déplacement | T=équipe | D=debug | ESC=quitter"
        help_surface = self.font.render(help_text, True, (255, 255, 255))
        self.screen.blit(help_surface, (10, self.screen_height - 30))
    
    def update_player_sprite(self, direction):
        """Met à jour la direction du sprite du joueur et active l'animation"""
        if direction in self.sprites:
            self.current_direction = direction
            self.is_moving = True
            self.animation_timer = pygame.time.get_ticks()
    
    def stop_player_animation(self):
        """Arrête l'animation du joueur"""
        self.is_moving = False
        self.current_frame = 0