import pygame
import os

# Initialisation de Pygame sans affichage
os.environ['SDL_VIDEODRIVER'] = 'dummy'
pygame.init()
pygame.display.set_mode((1, 1))

# Créer le dossier de destination
output_folder = "assets/sprites/mew/"
os.makedirs(output_folder, exist_ok=True)

# Chemin de la spritesheet
spritesheet_path = "assets/sprites/mew-sprite.png"
if not os.path.exists(spritesheet_path):
    print(f"❌ ERREUR : Sprite sheet introuvable à {spritesheet_path}")
    exit(1)

# Charger la spritesheet
spritesheet = pygame.image.load(spritesheet_path).convert()

# Définir la couleur de fond comme transparente (le vert)
bg_color = spritesheet.get_at((0, 0))
spritesheet.set_colorkey(bg_color)
print(f"🎨 Couleur de fond détectée: RGB{bg_color[:3]}")

# Dimensions de la spritesheet
sheet_width, sheet_height = spritesheet.get_size()
print(f"📊 Dimensions de la spritesheet: {sheet_width}x{sheet_height} pixels")

# La nouvelle spritesheet a 8 sprites alignés horizontalement
sprite_count = 8
sprite_width = sheet_width // sprite_count
sprite_height = sheet_height
print(f"🧩 Dimensions d'un sprite: {sprite_width}x{sprite_height} pixels")

# Correspondance entre position et direction
directions = {
    0: ("down", 0),   # Premier sprite: direction bas, frame 0
    1: ("down", 1),   # Deuxième sprite: direction bas, frame 1
    2: ("up", 0),     # etc.
    3: ("up", 1),
    4: ("left", 0),
    5: ("left", 1),
    6: ("right", 0),
    7: ("right", 1)
}

# Extraire et sauvegarder chaque sprite
for position, (direction, frame) in directions.items():
    # Coordonnées du sprite dans la spritesheet
    x = position * sprite_width
    
    # Créer une surface pour le sprite
    sprite = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
    
    # Copier la zone du sprite depuis la spritesheet
    sprite.blit(spritesheet, (0, 0), (x, 0, sprite_width, sprite_height))
    
    # Appliquer la transparence
    sprite.set_colorkey(bg_color)
    
    # Sauvegarder le sprite
    filename = f"{output_folder}mew_{direction}_frame{frame}.png"
    pygame.image.save(sprite, filename)
    print(f"✅ Sprite {filename} extrait")

print(f"\n✅ Extraction terminée! Les sprites sont prêts à être utilisés.")
pygame.quit()