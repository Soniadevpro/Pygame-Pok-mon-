import random

class Map:
    def __init__(self, width=20, height=10):
        self.width = width
        self.height = height
        
        # Initialiser toute la grille avec de l'eau (W)
        self.grid = [["W" for _ in range(width)] for _ in range(height)]
        
        # Créer une carte personnalisée avec un pont, des pontons, et des bâtiments
        # P = pont, M = ponton, C = pokecenter, S = pokeshop, A = arbre
        
        # Placer un pont traversant horizontalement au milieu
        pont_y = height // 2
        for x in range(2, width - 2):
            self.grid[pont_y][x] = "P"
            
        # Placer des pontons (bateaux) à gauche et à droite
        ponton_gauche_x, ponton_droite_x = 1, width - 2
        
        # Ponton à gauche (2x2)
        self.grid[pont_y - 1][ponton_gauche_x] = "M"
        self.grid[pont_y - 1][ponton_gauche_x + 1] = "M"
        self.grid[pont_y - 2][ponton_gauche_x] = "M"
        self.grid[pont_y - 2][ponton_gauche_x + 1] = "M"
        
        # Ponton à droite (2x2)
        self.grid[pont_y - 1][ponton_droite_x] = "M"
        self.grid[pont_y - 1][ponton_droite_x - 1] = "M"
        self.grid[pont_y - 2][ponton_droite_x] = "M"
        self.grid[pont_y - 2][ponton_droite_x - 1] = "M"
        
        # Placer le Pokecenter (3x2) sur la gauche
        pokecenter_x, pokecenter_y = width // 4, pont_y - 4
        for y in range(pokecenter_y, pokecenter_y + 2):
            for x in range(pokecenter_x, pokecenter_x + 3):
                if 0 <= y < height and 0 <= x < width:
                    self.grid[y][x] = "C"
                    
        # Placer le Pokeshop (3x2) sur la droite
        pokeshop_x, pokeshop_y = (width * 3) // 4, pont_y - 4
        for y in range(pokeshop_y, pokeshop_y + 2):
            for x in range(pokeshop_x, pokeshop_x + 3):
                if 0 <= y < height and 0 <= x < width:
                    self.grid[y][x] = "S"
                    
        # Ajouter quelques arbres autour pour l'esthétique
        # Sur le bord supérieur
        for x in range(0, width, 3):
            if x < width:
                self.grid[0][x] = "A"
        # Sur le bord inférieur
        for x in range(1, width, 4):
            if x < width:
                self.grid[height-1][x] = "A"
                
        # Ajouter une zone d'herbe (pour les rencontres de Pokémon)
        # Petite île d'herbe
        herbe_x, herbe_y = width // 2, pont_y + 2
        for y in range(herbe_y, min(herbe_y + 2, height)):
            for x in range(herbe_x - 2, min(herbe_x + 3, width)):
                if 0 <= y < height and 0 <= x < width:
                    self.grid[y][x] = "H"
    
    def is_grass(self, x, y):
        """Vérifie si la tuile à la position (x, y) est de l'herbe"""
        if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[y]):
            return self.grid[y][x] == "H"
        return False
    
    def is_walkable(self, x, y):
        """Vérifie si la tuile à la position (x, y) est praticable"""
        if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[y]):
            # Définir quelles tuiles sont praticables
            walkable_tiles = ["P", "M", "H"]  # Pont, Ponton et Herbe sont praticables
            return self.grid[y][x] in walkable_tiles
        return False
    
    def display(self):
        """Affiche la carte dans la console pour le débogage"""
        for row in self.grid:
            print("".join(row))
            