import random



class Map:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.grid = [["." for _ in range(width)] for _ in range(height)]
        self.generate_grass()
        
        self.grid = [
            ["A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A"],
            ["A", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "A"],
            ["A", "P", "H", "H", "H", "P", "M", "M", "M", "P", "C", "C", "C", "P", "S", "S", "S", "P", "P", "A"],
            ["A", "P", "H", "H", "H", "P", "M", "M", "M", "P", "C", "C", "C", "P", "S", "S", "S", "P", "P", "A"],
            ["A", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "P", "A"],
            ["A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A"],
        ]
    
        
        
    def generate_grass(self):
        
        for _ in range(int (self.width * self.height * 0.2)) : # 20% of the map is grass
            x, y = random.randint(0, self.width-1), random.randint(0, self.height-1)
            self.grid[y][x] = "G" # G for grass
            
            
    def is_grass(self, x, y):
        return self.grid[y][x] == "G"
        
        
    
    def is_wakable(self,x,y):
        return True
    
    
    def display(self):
        for row in self.grid:
            print("".join(row))
            