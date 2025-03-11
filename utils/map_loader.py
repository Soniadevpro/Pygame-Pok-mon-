import pygame
import pytmx
import pyscroll
import os

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
        
        # Créer un gestionnaire de rendu avec pyscroll avec mise à l'échelle
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(
            map_data, 
            (800, 600),  # Taille de la fenêtre de jeu
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
        """Met à jour le défilement de la carte en centrant sur le joueur"""
        try:
            # Calculer le centre de l'écran
            screen_center_x = 400  # Moitié de 800
            screen_center_y = 300  # Moitié de 600
            
            # Centrer la caméra sur le joueur
            self.group.center((screen_center_x, screen_center_y))
            
            # Ajuster la position de la vue pour suivre le joueur
            self.map_layer.set_center(
                player_rect.centerx, 
                player_rect.centery
            )
            
            # Mettre à jour le groupe
            self.group.update()
            
            print(f"🎮 Mise à jour de la caméra centrée sur {player_rect.center}")
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour de la caméra: {e}")
    
    def is_walkable(self, x, y):
        """Vérifie si la position (x, y) est praticable avec des logs détaillés"""
        # Calculer les limites de la carte en pixels
        map_width = self.width * self.real_tile_width
        map_height = self.height * self.real_tile_height
        
        print(f"\n🕹️ Vérification de praticabilité:")
        print(f"   Position pixel: ({x}, {y})")
        print(f"   Taille réelle de tuile: {self.real_tile_width}x{self.real_tile_height}")
        print(f"   Limites de la carte en pixels: {map_width}x{map_height}")
        
        # Vérifier les limites de la carte
        if (x < 0 or y < 0 or x >= map_width or y >= map_height):
            print(f"❌ Position ({x}, {y}) hors limites de la carte")
            return False
        
        # Convertir en coordonnées de tuile
        tile_x = int(x // self.real_tile_width)
        tile_y = int(y // self.real_tile_height)
        
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
                        walkable_gids = [2954, 2955, 3094, 3095, 5]  # Ajoutez les GID de vos tuiles de sol
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
        """Vérifie si la position (x, y) est dans l'herbe"""
        # Convertir en coordonnées de tuile
        tile_x = int(x // self.real_tile_width)
        tile_y = int(y // self.real_tile_height)
        
        # Vérifier les limites de la carte
        if (tile_x < 0 or tile_y < 0 or 
            tile_x >= self.width or tile_y >= self.height):
            return False
        
        # Vérifier chaque calque visible
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                try:
                    # Récupérer le GID de la tuile
                    gid = layer.data[tile_y][tile_x]
                    
                    # Vérifier les propriétés du calque
                    if hasattr(layer, 'properties'):
                        # Si le calque est marqué comme herbe
                        if layer.properties.get('type') == 'grass':
                            return True
                    
                    # Vérifier si la tuile est dans la liste des tuiles d'herbe
                    grass_gids = [2954, 2955, 3094, 3095, 5]  # Ajoutez les GID de vos tuiles d'herbe
                    if gid in grass_gids:
                        return True
                    
                except (IndexError, AttributeError, KeyError):
                    continue
        
        return False