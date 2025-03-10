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
            print(f"✅ Carte chargée: {filename}")
        except Exception as e:
            raise Exception(f"❌ Erreur lors du chargement de la carte: {e}")
        
        # Dimensions de la carte
        self.width = self.tmx_data.width
        self.height = self.tmx_data.height
        self.tile_width = self.tmx_data.tilewidth
        self.tile_height = self.tmx_data.tileheight
        print(f"📏 Dimensions carte : {self.width}x{self.height} tuiles.")
        
        # Facteur d'échelle pour agrandir les tuiles (passer de 16x16 à 40x40 par exemple)
        self.scale_factor = 2.5  # Ajustez cette valeur selon vos besoins
        
        # Créer un gestionnaire de rendu avec pyscroll avec mise à l'échelle
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(
            map_data, 
            (int(self.width * self.tile_width * self.scale_factor), 
             int(self.height * self.tile_height * self.scale_factor)),
            zoom=self.scale_factor  # Appliquer un zoom pour agrandir les tuiles
        )
        
        # Créer un groupe de sprites qui contient notre calque de carte
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer)
        
        # Stocker les informations sur les types de tuiles
        self.walkable_positions = []
        self.grass_positions = []
        self.water_positions = []
        self.building_positions = []
        
        # Points d'intérêt et points de spawn
        self.points_of_interest = {}
        
        # Analyser les propriétés des tuiles
        self._parse_map_properties()
        
        print(f"✅ Carte initialisée: {self.width}x{self.height} tuiles de {self.tile_width}x{self.tile_height}px (échelle: {self.scale_factor})")
    
    def _parse_map_properties(self):
        """Analyse les propriétés des tuiles et des objets de la carte"""
        # Parcourir tous les objets définis dans Tiled
        for obj in self.tmx_data.objects:
            if hasattr(obj, 'type') and obj.type == "player_start":
                # Stocker les coordonnées avec échelle appliquée
                self.points_of_interest["player_start"] = (
                    obj.x * self.scale_factor, 
                    obj.y * self.scale_factor
                )
                print(f"✅ Point de départ du joueur trouvé: ({obj.x}, {obj.y}) -> mise à l'échelle: ({obj.x * self.scale_factor}, {obj.y * self.scale_factor})")
            elif hasattr(obj, 'type') and obj.type in ["npc", "pokecenter", "pokeshop"]:
                self.points_of_interest[obj.name] = (
                    obj.x * self.scale_factor, 
                    obj.y * self.scale_factor, 
                    obj.type
                )
                print(f"✅ Point d'intérêt '{obj.name}' trouvé: ({obj.x}, {obj.y}) -> mise à l'échelle: ({obj.x * self.scale_factor}, {obj.y * self.scale_factor})")
        
        # Parcourir toutes les tuiles de tous les calques visibles
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'data'):  # Vérifier si c'est un calque de tuiles
                for x in range(self.width):
                    for y in range(self.height):
                        try:
                            tile_gid = layer.data[y][x]  # GID = Global ID de la tuile
                            if tile_gid:
                                # Récupérer les propriétés de la tuile
                                tile_props = self.tmx_data.get_tile_properties_by_gid(tile_gid)
                                if tile_props:
                                    # Convertir les positions en pixels avec échelle
                                    pixel_x = x * self.tile_width * self.scale_factor
                                    pixel_y = y * self.tile_height * self.scale_factor
                                    
                                    # Par défaut, toutes les tuiles sont marchables
                                    is_walkable = True
                                    
                                    # Vérifier les propriétés
                                    if 'walkable' in tile_props:
                                        is_walkable = tile_props.get('walkable') == 'true'
                                    
                                    if is_walkable:
                                        self.walkable_positions.append((pixel_x, pixel_y))
                                    
                                    # Vérifier le type de terrain
                                    tile_type = tile_props.get('type')
                                    if tile_type == 'grass':
                                        self.grass_positions.append((pixel_x, pixel_y))
                                    elif tile_type == 'water':
                                        self.water_positions.append((pixel_x, pixel_y))
                                    elif tile_type == 'building':
                                        self.building_positions.append((pixel_x, pixel_y))
                        except Exception as e:
                            print(f"⚠️ Erreur lors de l'analyse de la tuile ({x}, {y}): {e}")
        
        # Si aucune tuile n'a la propriété walkable='true', considérer toutes les tuiles comme praticables par défaut
        if not self.walkable_positions:
            print("⚠️ Aucune tuile avec propriété 'walkable' trouvée. Toutes les tuiles seront considérées comme praticables par défaut.")
            # Ajouter toutes les tuiles comme praticables
            for x in range(self.width):
                for y in range(self.height):
                    pixel_x = x * self.tile_width * self.scale_factor
                    pixel_y = y * self.tile_height * self.scale_factor
                    self.walkable_positions.append((pixel_x, pixel_y))
        
        print(f"✅ Nombre de positions praticables: {len(self.walkable_positions)}")
        print(f"✅ Nombre de positions d'herbe: {len(self.grass_positions)}")
    
    def get_spawn_position(self):
        """Retourne la position de départ du joueur ou une position par défaut"""
        if "player_start" in self.points_of_interest:
            return self.points_of_interest["player_start"]
        
        # Si aucun point de départ n'est défini, chercher une position praticable
        if self.walkable_positions:
            return self.walkable_positions[0]
        
        # Position par défaut au centre de la carte
        center_x = int(self.width * self.tile_width * self.scale_factor // 2)
        center_y = int(self.height * self.tile_height * self.scale_factor // 2)
        return (center_x, center_y)
    
    def render(self, screen):
        """Dessine la carte sur l'écran"""
        self.group.draw(screen)
    
    def update(self, player_rect):
        """Met à jour le défilement de la carte en centrant sur le joueur"""
        self.group.update()
        self.group.center(player_rect.center)
    
    def is_walkable(self, x, y):
        """Vérifie si la position (x, y) est praticable"""
        # Par défaut, autoriser tous les déplacements pour déboguer
        return True
        
        # Le code ci-dessous est commenté pour l'instant pour déboguer
        # Une fois que les déplacements fonctionnent, vous pourrez décommenter ce code
        
        """
        # Convertir en coordonnées de tuile en tenant compte du facteur d'échelle
        tile_x = int(x / (self.tile_width * self.scale_factor))
        tile_y = int(y / (self.tile_height * self.scale_factor))
        
        # Vérifier les limites de la carte
        if (tile_x < 0 or tile_y < 0 or 
            tile_x >= self.width or tile_y >= self.height):
            return False
        
        # Debugging
        print(f"Position en tuiles: ({tile_x}, {tile_y}), Position en pixels: ({x}, {y})")
        
        # Si nous avons une liste explicite de positions praticables, l'utiliser
        if self.walkable_positions:
            # Arrondir à la position de la tuile la plus proche
            aligned_x = tile_x * self.tile_width * self.scale_factor
            aligned_y = tile_y * self.tile_height * self.scale_factor
            
            # Vérifier si la position est dans la liste des positions praticables
            for walkable_x, walkable_y in self.walkable_positions:
                # Utiliser une tolérance pour la comparaison
                if (abs(walkable_x - aligned_x) < self.tile_width * self.scale_factor and
                    abs(walkable_y - aligned_y) < self.tile_height * self.scale_factor):
                    return True
            
            return False
        
        return True
        """
    
    def is_grass(self, x, y):
        """Vérifie si la position (x, y) est dans l'herbe"""
        # Simplifier pour le débogage - aucune herbe pour le moment
        return False
        
        # Le code ci-dessous est commenté pour l'instant pour déboguer
        """
        # Convertir en coordonnées de tuile en tenant compte du facteur d'échelle
        tile_x = int(x / (self.tile_width * self.scale_factor))
        tile_y = int(y / (self.tile_height * self.scale_factor))
        
        # Si nous avons une liste explicite de positions d'herbe, l'utiliser
        if self.grass_positions:
            # Arrondir à la position de la tuile la plus proche
            aligned_x = tile_x * self.tile_width * self.scale_factor
            aligned_y = tile_y * self.tile_height * self.scale_factor
            
            # Vérifier si la position est dans la liste des positions d'herbe
            for grass_x, grass_y in self.grass_positions:
                # Utiliser une tolérance pour la comparaison
                if (abs(grass_x - aligned_x) < self.tile_width * self.scale_factor and
                    abs(grass_y - aligned_y) < self.tile_height * self.scale_factor):
                    return True
            
            return False
        
        return False
        """