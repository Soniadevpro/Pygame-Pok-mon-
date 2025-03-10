import pygame

# Initialisation de Pygame
pygame.init()

# Chargement de l'image de l'arbre
image_path = "assets/tiles/arbre.png"
arbre = pygame.image.load(image_path)

# Création de la fenêtre
largeur, hauteur = 500, 500
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Test affichage arbre")

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Remplir l'écran avec un fond
    fenetre.fill((50, 150, 50))  # Vert foncé pour tester le fond transparent

    # Afficher l'arbre au centre
    arbre_rect = arbre.get_rect(center=(largeur // 2, hauteur // 2))
    fenetre.blit(arbre, arbre_rect)

    # Rafraîchir l'écran
    pygame.display.flip()

pygame.quit()
