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
        
        # Facteur d'échelle pour agrandir les tuiles (passer de 16x16 à 40x40 par exemple)
        self.scale_factor = 2.0  # Ajustez selon vos besoins
        
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
        
        # Listes pour stocker les types de tuiles
        self.walkable_tiles = []
        self.grass_tiles = []
        self.water_tiles = []
        self.building_tiles = []
        
        # Points d'intérêt
        self.points_of_interest = {}
        
        # Analyser les propriétés des tuiles
        self._parse_map_properties()
        
        print(f"✅ Carte Tiled initialisée avec un facteur d'échelle de {self.scale_factor}")
    
    def _parse_map_properties(self):
        """Analyse les propriétés des tuiles et des objets de la carte"""
        # Parcourir tous les objets définis dans Tiled
        print("🔍 Analyse des objets...")
        
        for obj in self.tmx_data.objects:
            if hasattr(obj, 'type') and obj.type == "player_start":
                self.points_of_interest["player_start"] = (
                    obj.x * self.scale_factor, 
                    obj.y * self.scale_factor
                )
                print(f"✅ Point de départ du joueur trouvé: ({obj.x}, {obj.y})")
        
        # Version simplifiée de l'analyse des tilesets
        try:
            # Pour l'instant, considérons toutes les tuiles comme praticables
            # pour éviter l'erreur "Element has no property tiles"
            print("⚠️ Toutes les tuiles seront considérées comme praticables.")
            for layer in self.tmx_data.visible_layers:
                if hasattr(layer, 'data'):
                    for y in range(self.height):
                        for x in range(self.width):
                            try:
                                # Si la tuile n'est pas vide (gid > 0), elle est praticable
                                if layer.data[y][x] > 0:
                                    # Ajouter à walkable_tiles car nous ne pouvons pas accéder aux propriétés
                                    self.walkable_tiles.append(layer.data[y][x])
                                    
                                    # Ajouter certains types spécifiques basés sur des heuristiques
                                    # Par exemple, si la tuile est verte, c'est probablement de l'herbe
                                    
                            except (IndexError, AttributeError):
                                continue
        except Exception as e:
            print(f"⚠️ Erreur lors de l'analyse des tilesets: {e}")
            print("⚠️ Utilisation des paramètres par défaut.")
    
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
            # Centrer la caméra sur le joueur
            self.group.center(player_rect.center)
            # Mettre à jour le groupe
            self.group.update()
            print(f"✅ Mise à jour de la caméra sur {player_rect.center}")
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour de la caméra: {e}")
    
    def is_walkable(self, x, y):
        """Vérifie si la position (x, y) est praticable"""
        # Convertir en coordonnées de tuile
        tile_x = int(x // self.real_tile_width)
        tile_y = int(y // self.real_tile_height)
        
        # Vérifier les limites de la carte
        if (tile_x < 0 or tile_y < 0 or 
            tile_x >= self.width or tile_y >= self.height):
            return False
        
        # Vérifier chaque calque pour la tuile à cette position
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                try:
                    # Récupérer le GID de la tuile
                    gid = layer.data[tile_y][tile_x]
                    
                    # Vérifier si la tuile est un obstacle ou une tuile praticable
                    if gid != 0:  # Tuile non vide
                        # Si c'est un obstacle (non praticable)
                        if gid not in self.walkable_tiles:
                            return False
                except (IndexError, AttributeError):
                    continue
        
        # Si on n'a pas trouvé d'obstacle, la position est praticable
        return True
    
    def is_grass(self, x, y):
        """Vérifie si la position (x, y) est dans l'herbe"""
        # Convertir en coordonnées de tuile
        tile_x = int(x // self.real_tile_width)
        tile_y = int(y // self.real_tile_height)
        
        # Vérifier les limites de la carte
        if (tile_x < 0 or tile_y < 0 or 
            tile_x >= self.width or tile_y >= self.height):
            return False
        
        # Vérifier chaque calque pour la tuile à cette position
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                try:
                    # Récupérer le GID de la tuile
                    gid = layer.data[tile_y][tile_x]
                    
                    # Vérifier si c'est une tuile d'herbe
                    if gid in self.grass_tiles:
                        return True
                except (IndexError, AttributeError):
                    continue
        
        # Si on n'a pas trouvé d'herbe, retourner False
        return False