from PIL import Image
import os

# 📌 Charger l'image sprite sheet
spritesheet_file = "../pokemon_game/assets/sprites/mew-sprite.png"

if not os.path.exists(spritesheet_file):
    print(f"❌ ERREUR : {spritesheet_file} introuvable ! Vérifie son emplacement.")
    exit()

# ✅ Ouvrir l'image avec transparence
img = Image.open(spritesheet_file).convert("RGBA")

# ✅ Créer le dossier de destination
output_folder = "assets/sprites/mew/"
os.makedirs(output_folder, exist_ok=True)

# ✅ Détection automatique de la largeur et hauteur d'un sprite
sprite_count = 8  # 8 images en ligne (2 par direction)
full_width, full_height = img.size
sprite_width = full_width // sprite_count  # Largeur d’un sprite
sprite_height = full_height - 10  # ✅ On enlève 10 pixels pour ne pas prendre les crédits en bas

# ✅ Définition des directions et des frames
sprite_coords = {
    "down": [0, 1],   # 2 images pour le bas
    "up": [2, 3],     # 2 images pour le haut
    "left": [4, 5],   # 2 images pour la gauche
    "right": [6, 7]   # 2 images pour la droite
}

# ✅ Fonction pour retirer le fond vert et rendre l'image transparente
def remove_background(img):
    """ Supprime le fond vert et le rend transparent """
    img = img.convert("RGBA")  # Assurer que l'image est bien en mode transparent
    datas = img.getdata()
    new_data = []

    for item in datas:
        r, g, b, a = item  # Récupère les valeurs RGBA
        # ✅ Détection plus précise des pixels verts (ajustable si besoin)
        if g > 150 and r < 120 and b < 120:
            new_data.append((0, 0, 0, 0))  # Transparent
        else:
            new_data.append(item)

    img.putdata(new_data)
    return img

# ✅ Extraction et sauvegarde des sprites corrigés
for direction, frames in sprite_coords.items():
    for i, frame_index in enumerate(frames):
        left = frame_index * sprite_width
        right = left + sprite_width
        top = 0
        bottom = sprite_height  # ✅ Ne prend pas toute la hauteur pour éviter les crédits

        try:
            sprite = img.crop((left, top, right, bottom))
            sprite = remove_background(sprite)  # Appliquer suppression du fond vert
            filename = f"{output_folder}mew_{direction}_frame{i}.png"
            sprite.save(filename)
            print(f"✅ Sprite {filename} extrait avec succès")
        except Exception as e:
            print(f"❌ Erreur extraction {direction} frame {i}: {e}")

# ✅ Vérification des fichiers extraits
print("\n📂 Vérification des fichiers extraits :")
extracted_files = os.listdir(output_folder)
for file in extracted_files:
    if file.endswith(".png"):
        print(f"- {file}")

if not extracted_files:
    print("⚠️ Aucun fichier extrait, vérifie `extract_sprites.py` !")


