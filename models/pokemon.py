# models/pokemon.py

class Pokemon:
    def __init__(self, name, hp, max_hp, attack, defense, sprite_path, sprite_path_back=None):
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.level = 5
        self.sprite_path = sprite_path 
        self.sprite_path = sprite_path  # ✅ Sprite de face (par défaut)
        self.sprite_path_back = sprite_path_back  # ✅ Sprite de dos (optionnel)

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def is_fainted(self):
        return self.hp <= 0

    def __str__(self):
        return f"{self.name} (Level {self.level}) HP: {self.hp}/{self.max_hp}"
