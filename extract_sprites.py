from PIL import Image
import os

# Charger l'image
img = Image.open("trainer_spritesheet.png")  # Assurez-vous que le nom corresponde à votre fichier

# Créer le dossier des sprites s'il n'existe pas
os.makedirs("assets/sprites", exist_ok=True)

# Taille d'un sprite
sprite_width = 16
sprite_height = 20

# Coordonnées des différents sprites
sprites_coords = {
    "down_static": (0, 0, sprite_width, sprite_height),
    "down_frame1": (sprite_width, 0, sprite_width, sprite_height),
    "down_frame2": (sprite_width*2, 0, sprite_width, sprite_height),
    
    "up_static": (0, sprite_height, sprite_width, sprite_height),
    "up_frame1": (sprite_width, sprite_height, sprite_width, sprite_height),
    "up_frame2": (sprite_width*2, sprite_height, sprite_width, sprite_height),
    
    "left_static": (0, sprite_height*2, sprite_width, sprite_height),
    "left_frame1": (sprite_width, sprite_height*2, sprite_width, sprite_height),
    "left_frame2": (sprite_width*2, sprite_height*2, sprite_width, sprite_height),
    
    "right_static": (0, sprite_height*3, sprite_width, sprite_height),
    "right_frame1": (sprite_width, sprite_height*3, sprite_width, sprite_height),
    "right_frame2": (sprite_width*2, sprite_height*3, sprite_width, sprite_height)
}

# Extraire et sauvegarder
for name, box in sprites_coords.items():
    sprite = img.crop(box)
    sprite.save(f"assets/sprites/walk_{name}.png")
    print(f"Sprite {name} extrait")