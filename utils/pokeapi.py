import requests
import os

def fetch_pokemon(pokemon_name):
    """Récupère les données et le sprite d'un Pokémon depuis PokéAPI."""
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Erreur : Pokémon {pokemon_name} non trouvé.")
        return None

    data = response.json()
    pokemon = {
        "name": data["name"].capitalize(),
        "hp": data["stats"][0]["base_stat"],
        "attack": data["stats"][1]["base_stat"],
        "defense": data["stats"][2]["base_stat"],
        "sprite": data["sprites"]["front_default"]
    }

    sprite_url = pokemon["sprite"]
    sprite_path = f"assets/sprites/{pokemon['name'].lower()}.png"

    if not os.path.exists("assets/sprites"):
        os.makedirs("assets/sprites")

    sprite_response = requests.get(sprite_url)
    if sprite_response.status_code == 200:
        with open(sprite_path, "wb") as file:
            file.write(sprite_response.content)
        print(f"Sprite de {pokemon['name']} téléchargé avec succès !")
        pokemon["sprite_path"] = sprite_path
    else:
        print(f"Erreur : impossible de télécharger le sprite de {pokemon['name']}.")
        pokemon["sprite_path"] = None
    
    return pokemon


def fetch_trainer_sprite(trainer_name):
    """Télécharge un sprite de dresseur depuis Pokémon Showdown."""
    base_url = "https://play.pokemonshowdown.com/sprites/trainers/"
    sprite_url = f"{base_url}{trainer_name.lower()}.png"

    sprite_path = f"assets/sprites/{trainer_name.lower()}.png"
    if not os.path.exists("assets/sprites"):
        os.makedirs("assets/sprites")

    response = requests.get(sprite_url)
    if response.status_code == 200:
        with open(sprite_path, "wb") as file:
            file.write(response.content)
        print(f"Sprite du dresseur {trainer_name} téléchargé avec succès !")
        return sprite_path
    else:
        print(f"Erreur : impossible de télécharger le sprite de {trainer_name}")
        return None
