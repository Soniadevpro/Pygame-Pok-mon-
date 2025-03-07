# models/player.py
from .pokemon import Pokemon

class Player:
    def __init__(self, name, position=(0, 0)):
        self.name = name
        self.position = position
        self.pokemons = []

    def add_pokemon(self, pokemon):
            if len(self.pokemons) < 6:
                self.pokemons.append(pokemon)
                return True
            else:
                print("Votre équipe est pleine !")
                return False
    
    def move(self, dx, dy):
        # Change la position en fonction du déplacement demandé
        x, y = self.position
        self.position = (x + dx, y + dy)

    def has_usable_pokemon(self):
        return any(pokemon.hp > 0 for pokemon in self.pokemons)

    def __str__(self):
        pokemons_str = ', '.join(str(p) for p in self.pokemons)
        return f"Joueur : {self.name}, Pokémon: [{pokemons_str}]"
