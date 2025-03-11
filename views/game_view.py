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
        
        # Variables pour l'effet des hautes herbes
        self.in_grass_effect = False
        self.grass_effect_timer = 0
        self.grass_effect_duration = 15  # Durée de l'effet en frames
        
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
            # En mode Tiled avec une caméra style Pokémon
            player_x, player_y = self.controller.player.position
            
            # Récupérer les coordonnées de la caméra
            camera_x = self.controller.map.camera_x
            camera_y = self.controller.map.camera_y
            
            # Calculer la position du joueur à l'écran
            screen_x = player_x - camera_x
            screen_y = player_y - camera_y
            
            # Dessiner le joueur à la position relative à l'écran
            sprite_rect = current_sprite.get_rect()
            sprite_rect.centerx = screen_x
            sprite_rect.centery = screen_y
            self.screen.blit(current_sprite, sprite_rect)
            
            # Debug - afficher des informations supplémentaires
            if self.controller.debug_movement:
                # Position du joueur à l'écran
                pygame.draw.circle(self.screen, (255, 0, 0), (int(screen_x), int(screen_y)), 3)
                
                # Coordonnées du joueur
                pos_text = f"Pos: ({player_x}, {player_y})"
                pos_surf = self.font.render(pos_text, True, (255, 255, 0))
                self.screen.blit(pos_surf, (10, self.screen_height - 60))
                
                # Coordonnées caméra
                cam_text = f"Cam: ({int(camera_x)}, {int(camera_y)})"
                cam_surf = self.font.render(cam_text, True, (255, 255, 0))
                self.screen.blit(cam_surf, (10, self.screen_height - 30))
                
                # Zone limite où la caméra commence à suivre le joueur
                edge_margin_x = self.screen_width * 0.25
                edge_margin_y = self.screen_height * 0.25
                
                # Rectangle montrant la zone "morte" où la caméra ne bouge pas
                pygame.draw.rect(self.screen, (0, 255, 0), 
                                (edge_margin_x, edge_margin_y, 
                                 self.screen_width - (2 * edge_margin_x), 
                                 self.screen_height - (2 * edge_margin_y)), 
                                 2)
        else:
            # En mode traditionnel, le joueur est à sa position absolue
            player_x, player_y = self.controller.player.position
            self.screen.blit(current_sprite, (player_x, player_y))
        
        # Vérifier si le joueur est dans les hautes herbes
        is_in_grass = False
        if self.controller.using_tiled:
            is_in_grass = self.controller.map.is_grass(player_x, player_y)
        else:
            grid_x = player_x // self.tile_size
            grid_y = player_y // self.tile_size
            if 0 <= grid_x < self.controller.map.width and 0 <= grid_y < self.controller.map.height:
                is_in_grass = self.controller.map.is_grass(grid_x, grid_y)
        
        # Effet visuel lorsque le joueur est dans les hautes herbes
        if is_in_grass and self.is_moving:
            # Activer l'effet
            self.in_grass_effect = True
            self.grass_effect_timer = self.grass_effect_duration
        
        # Gérer l'effet des hautes herbes
        if self.in_grass_effect and self.grass_effect_timer > 0:
            # Dessiner de petits points verts autour du joueur
            if self.controller.using_tiled:
                screen_x = player_x - self.controller.map.camera_x
                screen_y = player_y - self.controller.map.camera_y
            else:
                screen_x, screen_y = player_x, player_y
            
            # Points aléatoires autour du joueur
            for _ in range(3):
                offset_x = random.randint(-10, 10)
                offset_y = random.randint(-10, 10)
                point_x = int(screen_x + offset_x)
                point_y = int(screen_y + offset_y)
                
                # Dessiner un petit point vert
                pygame.draw.circle(self.screen, (0, 200, 0), (point_x, point_y), 1)
            
            # Diminuer le timer de l'effet
            self.grass_effect_timer -= 1
            if self.grass_effect_timer <= 0:
                self.in_grass_effect = False
        
        # Afficher les informations de débogage
        self._draw_debug_info()
    
    def _render_tiled_map(self):
        """Affiche la carte Tiled"""
        if hasattr(self.controller.map, 'render'):
            try:
                # Appliquer les mises à jour du groupe avant de rendre
                self.controller.map.group.update()
                
                # Rendre la carte avec le groupe mis à jour
                self.controller.map.group.draw(self.screen)
                
                # Affichage de débogage pour visualiser la position
                if self.controller.debug_movement:
                    center_x = self.screen_width // 2
                    center_y = self.screen_height // 2
                    # Dessiner une grille pour aider à visualiser le mouvement
                    for x in range(0, self.screen_width, self.tile_size):
                        pygame.draw.line(self.screen, (100, 100, 100), (x, 0), (x, self.screen_height), 1)
                    for y in range(0, self.screen_height, self.tile_size):
                        pygame.draw.line(self.screen, (100, 100, 100), (0, y), (self.screen_width, y), 1)
            except Exception as e:
                print(f"❌ Erreur lors du rendu de la carte Tiled: {e}")
                import traceback
                traceback.print_exc()
                self.screen.fill((135, 206, 235))  # Bleu ciel en cas d'erreur
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
        
        # Indication si le joueur est dans l'herbe
        is_in_grass = self.controller.map.is_grass(player_x, player_y) if self.controller.using_tiled else False
        grass_text = f"Dans l'herbe: {'Oui' if is_in_grass else 'Non'}"
        grass_surface = self.font.render(grass_text, True, (0, 255, 0) if is_in_grass else (255, 255, 255))
        self.screen.blit(grass_surface, (10, 130))
        
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