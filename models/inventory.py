class Inventory:
    def __init__(self):
        self.items = {"Pokeball": 5, "Potion": 2}
        
    def add_item(self, item, quantity):
        if item in self.items:
            self.items[item] += quantity
        else:
            self.items[item] = quantity
            
            
    def use_item(self, item):
        if self.tems.get(item, 0) > 0:
            self.items[item] -= 1
            return True
        return False
    
    
    def __str__(self):
        return ', '.join([f"{item} x{qty}" for item, qty in self.items.items()])