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
        
        # Créer un gestionnaire de rendu avec pyscroll
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(
            map_data, 
            (self.width * self.tile_width, self.height * self.tile_height)
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
        
        print(f"✅ Carte initialisée: {self.width}x{self.height} tuiles de {self.tile_width}x{self.tile_height}px")
    
    def _parse_map_properties(self):
        """Analyse les propriétés des tuiles et des objets de la carte"""
        # Parcourir tous les objets définis dans Tiled
        for obj in self.tmx_data.objects:
            if obj.type == "player_start":
                self.points_of_interest["player_start"] = (obj.x, obj.y)
                print(f"✅ Point de départ du joueur trouvé: ({obj.x}, {obj.y})")
            elif obj.type == "npc" or obj.type == "pokecenter" or obj.type == "pokeshop":
                self.points_of_interest[obj.name] = (obj.x, obj.y, obj.type)
                print(f"✅ Point d'intérêt '{obj.name}' trouvé: ({obj.x}, {obj.y})")
        
        # Parcourir toutes les tuiles de tous les calques visibles
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'data'):  # Vérifier si c'est un calque de tuiles
                for x in range(self.width):
                    for y in range(self.height):
                        tile_gid = layer.data[y][x]  # GID = Global ID de la tuile
                        if tile_gid:
                            # Récupérer les propriétés de la tuile
                            tile_props = self.tmx_data.get_tile_properties_by_gid(tile_gid)
                            if tile_props:
                                # Convertir les positions en pixels
                                pixel_x = x * self.tile_width
                                pixel_y = y * self.tile_height
                                
                                # Vérifier les propriétés
                                if tile_props.get('walkable') == 'true':
                                    self.walkable_positions.append((pixel_x, pixel_y))
                                
                                # Vérifier le type de terrain
                                tile_type = tile_props.get('type')
                                if tile_type == 'grass':
                                    self.grass_positions.append((pixel_x, pixel_y))
                                elif tile_type == 'water':
                                    self.water_positions.append((pixel_x, pixel_y))
                                elif tile_type == 'building':
                                    self.building_positions.append((pixel_x, pixel_y))
        
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
        return (self.width * self.tile_width // 2, self.height * self.tile_height // 2)
    
    def render(self, screen):
        """Dessine la carte sur l'écran"""
        self.group.draw(screen)
    
    def update(self, player_rect):
        """Met à jour le défilement de la carte en centrant sur le joueur"""
        self.group.update()
        self.group.center(player_rect.center)
    
    def is_walkable(self, x, y):
        """Vérifie si la position (x, y) est praticable"""
        # Convertir en coordonnées de tuile
        tile_x = x // self.tile_width
        tile_y = y // self.tile_height
        
        # Vérifier les limites de la carte
        if (tile_x < 0 or tile_y < 0 or 
            tile_x >= self.width or tile_y >= self.height):
            return False
        
        # Si nous avons une liste explicite de positions praticables, l'utiliser
        if self.walkable_positions:
            # Arrondir à la position de la tuile la plus proche
            aligned_x = (x // self.tile_width) * self.tile_width
            aligned_y = (y // self.tile_height) * self.tile_height
            return (aligned_x, aligned_y) in self.walkable_positions
        
        # Sinon, considérer que tout est praticable sauf les collisions explicites
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                # Récupérer la tuile à cette position
                tile_gid = layer.data[tile_y][tile_x]
                if tile_gid:
                    # Vérifier si la tuile a une propriété de collision
                    props = self.tmx_data.get_tile_properties_by_gid(tile_gid)
                    if props and props.get('walkable') == 'false':
                        return False
        
        return True
    
    def is_grass(self, x, y):
        """Vérifie si la position (x, y) est dans l'herbe"""
        # Si nous avons une liste explicite de positions d'herbe, l'utiliser
        if self.grass_positions:
            # Arrondir à la position de la tuile la plus proche
            aligned_x = (x // self.tile_width) * self.tile_width
            aligned_y = (y // self.tile_height) * self.tile_height
            return (aligned_x, aligned_y) in self.grass_positions
        
        # Convertir en coordonnées de tuile
        tile_x = x // self.tile_width
        tile_y = y // self.tile_height
        
        # Vérifier les limites de la carte
        if (tile_x < 0 or tile_y < 0 or 
            tile_x >= self.width or tile_y >= self.height):
            return False
        
        # Vérifier chaque calque
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                # Récupérer la tuile à cette position
                tile_gid = layer.data[tile_y][tile_x]
                if tile_gid:
                    # Vérifier si la tuile a une propriété de type "grass"
                    props = self.tmx_data.get_tile_properties_by_gid(tile_gid)
                    if props and props.get('type') == 'grass':
                        return True
        
        return False