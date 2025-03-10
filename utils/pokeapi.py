import requests
import os

API_URL = "https://pokeapi.co/api/v2/pokemon/"


def fetch_pokemon(pokemon_name):
    """Récupère les données et les sprites d'un Pokémon depuis PokéAPI."""
    
    url = f"{API_URL}{pokemon_name.lower()}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"❌ Erreur : Pokémon {pokemon_name} non trouvé sur PokéAPI.")
        return None

    data = response.json()
    pokemon = {
        "name": data["name"].capitalize(),
        "hp": data["stats"][0]["base_stat"],
        "attack": data["stats"][1]["base_stat"],
        "defense": data["stats"][2]["base_stat"],
        "sprite_front": data["sprites"]["front_default"],  # ✅ Sprite de face (Pokémon sauvage)
        "sprite_back": data["sprites"]["back_default"]  # ✅ Sprite de dos (Pokémon du joueur)
    }

    if not pokemon["sprite_front"]:
        print(f"⚠️ Aucun sprite de face trouvé pour {pokemon_name}.")
        return None

    if not pokemon["sprite_back"]:
        print(f"⚠️ Aucun sprite de dos trouvé pour {pokemon_name}.")

    # ✅ Définir les chemins d'enregistrement
    sprite_dir = "assets/sprites"
    if not os.path.exists(sprite_dir):
        os.makedirs(sprite_dir)

    front_sprite_path = f"{sprite_dir}/{pokemon['name'].lower()}_front.png"
    back_sprite_path = f"{sprite_dir}/{pokemon['name'].lower()}_back.png"

    # ✅ Télécharger le sprite de face (Pokémon sauvage)
    if pokemon["sprite_front"] and not os.path.exists(front_sprite_path):
        sprite_response = requests.get(pokemon["sprite_front"])
        if sprite_response.status_code == 200:
            with open(front_sprite_path, "wb") as file:
                file.write(sprite_response.content)
            print(f"✅ Sprite de face de {pokemon['name']} téléchargé !")
        else:
            print(f"❌ Erreur lors du téléchargement du sprite de face de {pokemon['name']}.")

    # ✅ Télécharger le sprite de dos (Pokémon du joueur)
    if pokemon["sprite_back"] and not os.path.exists(back_sprite_path):
        sprite_response = requests.get(pokemon["sprite_back"])
        if sprite_response.status_code == 200:
            with open(back_sprite_path, "wb") as file:
                file.write(sprite_response.content)
            print(f"✅ Sprite de dos de {pokemon['name']} téléchargé !")
        else:
            print(f"❌ Erreur lors du téléchargement du sprite de dos de {pokemon['name']}.")

    # ✅ Ajouter les chemins aux données du Pokémon
    pokemon["sprite_path_front"] = front_sprite_path
    pokemon["sprite_path_back"] = back_sprite_path

    return pokemon


def fetch_trainer_sprite(trainer_name):
    """Télécharge un sprite de dresseur depuis Pokémon Showdown."""
    
    base_url = "https://play.pokemonshowdown.com/sprites/trainers/"
    sprite_url = f"{base_url}{trainer_name.lower()}.png"
    sprite_path = f"assets/sprites/{trainer_name.lower()}.png"

    if not os.path.exists(sprite_path):
        if not os.path.exists("assets/sprites"):
            os.makedirs("assets/sprites")

        response = requests.get(sprite_url)
        if response.status_code == 200:
            with open(sprite_path, "wb") as file:
                file.write(response.content)
            print(f"✅ Sprite du dresseur {trainer_name} téléchargé avec succès !")
        else:
            print(f"❌ Erreur : impossible de télécharger le sprite de {trainer_name}.")
            return None

    return sprite_path

