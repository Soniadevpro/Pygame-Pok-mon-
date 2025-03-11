import pygame
import pytmx
import pyscroll
import os
import random

class TiledMap:
    def __init__(self, filename):
        """Charge une carte depuis un fichier TMX créé avec Tiled"""
        # Vérifier que le fichier existe
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Le fichier de carte {filename} n'existe pas.")
        
        # S'assurer que Pygame est initialisé avec un mode vidéo
        if not pygame.get_init():
            pygame.init()
        if pygame.display.get_surface() is None:
            temp_surface = pygame.display.set_mode((1, 1))
        
        # Taille de l'écran pour le centrage de la caméra
        self.screen_width = 800
        self.screen_height = 600
        
        # Variables pour stocker la position de la caméra
        self.camera_x = 0
        self.camera_y = 0
        
        # Charger les données de la carte TMX
        try:
            self.tmx_data = pytmx.load_pygame(filename, pixelalpha=True)
            print(f"✅ Carte Tiled chargée: {filename}")
        except Exception as e:
            raise Exception(f"❌ Erreur lors du chargement de la carte: {e}")
        
        # Dimensions de la carte
        self.width = self.tmx_data.width
        self.height = self.tmx_data.height
        self.tile_width = self.tmx_data.tilewidth
        self.tile_height = self.tmx_data.tileheight
        print(f"📏 Dimensions carte : {self.width}x{self.height} tuiles de {self.tile_width}x{self.tile_height}px")
        
        # Facteur d'échelle pour agrandir les tuiles
        self.scale_factor = 2.0
        
        # Taille réelle d'une tuile après mise à l'échelle
        self.real_tile_width = int(self.tile_width * self.scale_factor)
        self.real_tile_height = int(self.tile_height * self.scale_factor)
        
        # Calculer les dimensions réelles de la carte en pixels
        self.map_width_px = self.width * self.real_tile_width
        self.map_height_px = self.height * self.real_tile_height
        print(f"📏 Dimensions carte en pixels : {self.map_width_px}x{self.map_height_px}")
        
        # Détecter automatiquement les offsets si nécessaire
        # Ces valeurs peuvent être ajustées pour compenser les décalages
        self.offset_x = 0
        self.offset_y = 0
        
        # IMPORTANT: NE PAS réduire la hauteur de la carte
        # self.map_height_px -= 2 * self.real_tile_height  # Cette ligne a été supprimée
        
        # Créer un gestionnaire de rendu avec pyscroll avec mise à l'échelle
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(
            map_data, 
            (self.screen_width, self.screen_height),  # Utiliser les variables de classe
            zoom=self.scale_factor
        )
        
        # Créer un groupe de sprites qui contient notre calque de carte
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer)
        
        # Points d'intérêt
        self.points_of_interest = {}
        
        # Points de départ et zones spéciales
        self._parse_map_objects()
        
        print(f"✅ Carte Tiled initialisée avec un facteur d'échelle de {self.scale_factor}")
    
    def _parse_map_objects(self):
        """Analyse les objets et points d'intérêt de la carte"""
        print("🔍 Analyse des objets de la carte...")
        
        # Parcourir tous les objets
        for obj in self.tmx_data.objects:
            # Point de départ du joueur
            if hasattr(obj, 'type') and obj.type == "player_start":
                self.points_of_interest["player_start"] = (
                    obj.x * self.scale_factor, 
                    obj.y * self.scale_factor
                )
                print(f"✅ Point de départ du joueur trouvé: ({obj.x}, {obj.y})")
    
    def get_spawn_position(self):
        """Retourne la position de départ du joueur ou une position par défaut"""
        if "player_start" in self.points_of_interest:
            return self.points_of_interest["player_start"]
        
        # Position par défaut au centre de la carte
        center_x = int(self.width * self.real_tile_width // 2)
        center_y = int(self.height * self.real_tile_height // 2)
        return (center_x, center_y)
    
    def render(self, screen):
        """Dessine la carte sur l'écran"""
        self.group.draw(screen)
    
    def update(self, player_rect):
        """
        Met à jour la caméra style Pokémon: le joueur se déplace librement 
        et la caméra ne bouge que lorsqu'il s'approche des bords
        """
        try:
            # Récupérer les coordonnées du joueur
            player_x, player_y = player_rect.centerx, player_rect.centery
            
            # --- Logique de caméra style Pokémon ---
            # Ne déplacer la caméra que lorsque le joueur s'approche des bords
            # Zones de déclenchement des bords (25% de l'écran depuis les bords)
            edge_margin_x = self.screen_width * 0.25
            edge_margin_y = self.screen_height * 0.25
            
            # Initialiser les variables de caméra si ce n'est pas déjà fait
            if not hasattr(self, 'camera_x') or not hasattr(self, 'camera_y'):
                self.camera_x = player_x - (self.screen_width // 2)
                self.camera_y = player_y - (self.screen_height // 2)
            
            # Position du joueur par rapport à l'écran
            screen_x = player_x - self.camera_x
            screen_y = player_y - self.camera_y
            
            # Vérifier si le joueur s'approche des bords et ajuster la caméra
            camera_moved = False
            
            # Bord droit
            if screen_x > self.screen_width - edge_margin_x:
                self.camera_x = player_x - (self.screen_width - edge_margin_x)
                camera_moved = True
            
            # Bord gauche
            elif screen_x < edge_margin_x:
                self.camera_x = player_x - edge_margin_x
                camera_moved = True
            
            # Bord inférieur
            if screen_y > self.screen_height - edge_margin_y:
                self.camera_y = player_y - (self.screen_height - edge_margin_y)
                camera_moved = True
            
            # Bord supérieur
            elif screen_y < edge_margin_y:
                self.camera_y = player_y - edge_margin_y
                camera_moved = True
            
            # Limiter la caméra aux bords de la carte en tenant compte de l'écran
            # Utiliser les dimensions réelles de la carte avec les offsets
            self.camera_x = max(0 - self.offset_x, min(self.camera_x, self.map_width_px - self.screen_width + self.offset_x))
            self.camera_y = max(0 - self.offset_y, min(self.camera_y, self.map_height_px - self.screen_height + self.offset_y))
            
            # Mettre à jour la position de la caméra
            if camera_moved:
                # Appliquer la nouvelle position caméra
                camera_center_x = self.camera_x + (self.screen_width // 2)
                camera_center_y = self.camera_y + (self.screen_height // 2)
                
                # Utiliser la méthode center avec un tuple pour déplacer la caméra
                self.map_layer.center((camera_center_x, camera_center_y))
                
                # Mettre à jour le groupe
                self.group.update()
                
                print(f"🎮 Caméra déplacée - Position: ({self.camera_x}, {self.camera_y})")
            
            # Afficher occasionnellement les infos de débogage
            if random.random() < 0.02:  # 2% du temps
                self.debug_print_map_state()
                
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour de la caméra: {e}")
            import traceback
            traceback.print_exc()
    
    def debug_print_map_state(self):
        """Affiche les informations de débogage sur l'état actuel de la carte"""
        print("\n===== DEBUG MAP STATE =====")
        print(f"Map dimensions: {self.width}x{self.height} tiles ({self.map_width_px}x{self.map_height_px} px)")
        print(f"Camera position: ({self.camera_x}, {self.camera_y})")
        print(f"Offsets: X={self.offset_x}, Y={self.offset_y}")
        print("==========================\n")
    
    def is_walkable(self, x, y):
        """Vérifie si la position (x, y) est praticable avec des logs détaillés"""
        # Calculer les limites de la carte en pixels
        map_width = self.map_width_px
        map_height = self.map_height_px
        
        print(f"\n🕹️ Vérification de praticabilité:")
        print(f"   Position pixel: ({x}, {y})")
        print(f"   Taille réelle de tuile: {self.real_tile_width}x{self.real_tile_height}")
        print(f"   Limites de la carte en pixels: {map_width}x{map_height}")
        
        # Pour la vérification de praticabilité, utiliser une plus grande tolérance
        # aux bords de la carte pour éviter les faux-positifs "hors limites"
        margin = 20  # pixels de tolérance
        
        # Vérifier les limites de la carte avec la marge de tolérance
        if (x < -margin or y < -margin or 
            x >= map_width + margin or y >= map_height + margin):
            print(f"❌ Position ({x}, {y}) hors limites de la carte")
            return False
        
        # Convertir en coordonnées de tuile
        tile_x = int(x // self.real_tile_width)
        tile_y = int(y // self.real_tile_height)
        
        # Limiter les coordonnées de tuile aux dimensions de la carte
        tile_x = max(0, min(tile_x, self.width - 1))
        tile_y = max(0, min(tile_y, self.height - 1))
        
        print(f"   Position tuile: ({tile_x}, {tile_y})")
        
        # Vérifier chaque calque visible
        walkable_found = False
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                try:
                    # Récupérer le GID de la tuile
                    gid = layer.data[tile_y][tile_x]
                    
                    print(f"   Calque: {layer.name}")
                    print(f"   GID de la tuile: {gid}")
                    
                    # Vérifier les propriétés du calque
                    if hasattr(layer, 'properties'):
                        print(f"   Propriétés du calque: {layer.properties}")
                        # Si le calque est marqué comme praticable
                        if layer.properties.get('walkable', False):
                            print("   ✅ Calque marqué comme praticable")
                            walkable_found = True
                    
                    # Vérifier si la tuile est non vide
                    if gid != 0:
                        # Mode permissif : considérer certaines tuiles comme praticables
                        # Liste des GID que vous savez être praticables
                        walkable_gids = [2954, 2955, 3094, 3095, 5, 2]  # Ajoutez les GID de vos tuiles de sol
                        if gid in walkable_gids:
                            print(f"   ✅ GID {gid} considéré comme praticable par défaut")
                            walkable_found = True
                    
                    # Si on a trouvé une tuile praticable, on peut arrêter de chercher
                    if walkable_found:
                        break
                    
                except (IndexError, AttributeError, KeyError) as e:
                    print(f"   Erreur lors de la vérification: {e}")
        
        print(f"   Résultat final: {'Praticable' if walkable_found else 'Non praticable'}")
        return walkable_found

    def is_grass(self, x, y):
        """Vérifie si la position (x, y) est dans les hautes herbes"""
        # Convertir en coordonnées de tuile
        tile_x = int(x // self.real_tile_width)
        tile_y = int(y // self.real_tile_height)
        
        # Vérifier les limites de la carte
        if (tile_x < 0 or tile_y < 0 or 
            tile_x >= self.width or tile_y >= self.height):
            return False
        
        # Vérification 1: Rechercher un calque spécifique nommé "hautes_herbes"
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'name') and layer.name == "hautes_herbes":
                if hasattr(layer, 'data'):
                    try:
                        # Récupérer le GID de la tuile
                        gid = layer.data[tile_y][tile_x]
                        
                        # Si la tuile n'est pas vide (GID > 0), c'est de l'herbe
                        if gid > 0:
                            print(f"🌿 Détection herbe dans calque 'hautes_herbes': GID {gid}")
                            return True
                            
                    except (IndexError, AttributeError, KeyError) as e:
                        print(f"Erreur lors de la vérification du calque 'hautes_herbes': {e}")
        
        # Vérification 2: Rechercher un calque avec type='haute_herbe'
        # (différent de 'grass' pour éviter la confusion avec le sol)
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'properties') and layer.properties.get('type') == 'haute_herbe':
                if hasattr(layer, 'data'):
                    try:
                        # Récupérer le GID de la tuile
                        gid = layer.data[tile_y][tile_x]
                        
                        # Si la tuile n'est pas vide (GID > 0), c'est de l'herbe
                        if gid > 0:
                            print(f"🌿 Détection herbe dans calque de type 'haute_herbe': GID {gid}")
                            return True
                            
                    except (IndexError, AttributeError, KeyError) as e:
                        print(f"Erreur lors de la vérification du calque de type 'haute_herbe': {e}")
        
        # Pas d'herbe haute détectée
        return False