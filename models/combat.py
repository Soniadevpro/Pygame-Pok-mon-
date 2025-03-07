# models/combat.py
import random

class Combat:
    def __init__(self, player_pokemon, wild_pokemon):
        self.player_pokemon = player_pokemon
        self.wild_pokemon = wild_pokemon

    def player_attack(self):
    # Calcul des dégâts plus doux (30% des PV restants du Pokémon sauvage max)
        damage = max(1, int((self.wild_pokemon.max_hp / 3) * random.uniform(0.2, 0.5)))
        self.wild_pokemon.hp -= damage
        self.wild_pokemon.hp = max(0, self.wild_pokemon.hp)  # Empêche les HP négatifs
        return damage


    def wild_attack(self):
        damage = max(1, self.wild_pokemon.attack - self.player_pokemon.defense)
        self.player_pokemon.hp -= damage
        return damage

    def player_run(self):
        # 50% de chance de fuite réussie
        return random.random() < 0.5

    def attempt_capture(self, inventory):
        if inventory.use_item("Pokeball"):
            capture_chance = (self.wild_pokemon.max_hp - self.wild_pokemon.hp) / self.wild_pokemon.max_hp
            success = random.random() < capture_chance
            return success
        else:
            print("Vous n'avez pas de Pokéball !")
            return False
        
    def is_over(self):
        return self.player_pokemon.is_fainted() or self.wild_pokemon.is_fainted()