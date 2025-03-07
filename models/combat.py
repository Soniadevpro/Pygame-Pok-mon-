# models/combat.py
import random

class Combat:
    def __init__(self, player_pokemon, wild_pokemon):
        self.player_pokemon = player_pokemon
        self.wild_pokemon = wild_pokemon

    def player_attack(self):
        damage = max(1, self.player_pokemon.attack - self.wild_pokemon.defense)
        self.wild_pokemon.hp -= damage
        return damage

    def wild_attack(self):
        damage = max(1, self.wild_pokemon.attack - self.player_pokemon.defense)
        self.player_pokemon.hp -= damage
        return damage

    def player_run(self):
        # 50% de chance de fuite réussie
        return random.random() < 0.5

    def is_over(self):
        return self.player_pokemon.is_fainted() or self.wild_pokemon.is_fainted()

    
    
    