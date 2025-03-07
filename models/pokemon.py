# models/pokemon.py

class Pokemon:
    def __init__(self, name, hp, max_hp, attack, defense, level=5, sprite_path=None):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.level = 5
        self.sprite_path = sprite_path 
        

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def is_fainted(self):
        return self.hp <= 0

    def __str__(self):
        return f"{self.name} (Level {self.level}) HP: {self.hp}/{self.max_hp}"
