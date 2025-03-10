import os
os.environ["SDL_VIDEODRIVER"] = "dummy"  # ✅ Évite l'erreur "No video mode has been set"
import pygame

# Configuration
spritesheet_path = "assets/tiles/pokemon_tiles.png"
output_folder = "assets/tiles/"
tile_size = 32  # ⚠️ Ajuste selon ta spritesheet !

# Vérification du fichier
if not os.path.exists(spritesheet_path):
    print(f"❌ ERREUR : Fichier {spritesheet_path} introuvable.")
    exit(1)

# Initialisation de Pygame
pygame.init()
pygame.display.set_mode((1, 1))  # ✅ Simule un écran minimal pour éviter l'erreur

# Charger la spritesheet
spritesheet = pygame.image.load(spritesheet_path).convert_alpha()

# Détection automatique du nombre de colonnes et lignes
sheet_width, sheet_height = spritesheet.get_size()
cols = sheet_width // tile_size
rows = sheet_height // tile_size

# Création du dossier de sortie s'il n'existe pas
os.makedirs(output_folder, exist_ok=True)

# Extraire et sauvegarder les tuiles
for y in range(rows):
    for x in range(cols):
        tile = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
        tile.blit(spritesheet, (0, 0), (x * tile_size, y * tile_size, tile_size, tile_size))

        # Sauvegarde sous forme de `tile_x_y.png`
        filename = f"{output_folder}tile_{x}_{y}.png"
        pygame.image.save(tile, filename)
        print(f"✅ Tuile enregistrée : {filename}")

pygame.quit()
print("\n✅ Extraction terminée !")

