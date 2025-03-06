# models/pokemon.py

class Pokemon:
    def __init__(self, name, hp, max_hp, attack, defense, level=5):
        self.name = name
        self.level = level
        self.hp = hp
        self.max_hp = max_hp
        self.attack = attack
        self.defense = defense

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def is_fainted(self):
        return self.hp <= 0

    def __str__(self):
        return f"{self.name} (Level {self.level}) HP: {self.hp}/{self.max_hp}"
