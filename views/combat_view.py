import pygame

class CombatView:
    def __init__(self, controller, combat):
        self.controller = controller
        self.combat = combat
        self.screen = controller.view.screen
        self.font = pygame.font.Font(None, 24)
        
        # ✅ Charger les sprites des Pokémon
        self.player_pokemon_sprite = pygame.image.load(combat.player_pokemon.sprite_path_back if combat.player_pokemon.sprite_path_back else combat.player_pokemon.sprite_path).convert_alpha()

        self.wild_pokemon_sprite = pygame.image.load(combat.wild_pokemon.sprite_path).convert_alpha()
        
        # ✅ Redimensionner les sprites
        self.player_pokemon_sprite = pygame.transform.scale(self.player_pokemon_sprite, (100, 100))
        self.wild_pokemon_sprite = pygame.transform.scale(self.wild_pokemon_sprite, (100, 100))

        # ✅ Position des Pokémon
        self.player_pos = (50, 250)  # Mew en bas à gauche
        self.wild_pos = (250, 50)  # Pokémon sauvage en haut à droite
        
        # ✅ Animation
        self.attack_animation = False
        self.animation_timer = 0
        self.animation_offset = 0

        # ✅ Création des boutons
        self.button_font = pygame.font.Font(None, 30)
        self.buttons = {
            "attack": pygame.Rect(50, 400, 120, 40),
            "capture": pygame.Rect(200, 400, 120, 40),
            "run": pygame.Rect(350, 400, 120, 40)
        }

    def render(self):
        """ Affichage de l'écran de combat """
        self.screen.fill((30, 30, 30))  # Fond noir

        # ✅ Afficher les Pokémon
        self.screen.blit(self.wild_pokemon_sprite, (self.wild_pos[0], self.wild_pos[1] + self.animation_offset))
        self.screen.blit(self.player_pokemon_sprite, (self.player_pos[0], self.player_pos[1] - self.animation_offset))

        # ✅ Affichage des HP
        self.draw_hp_bar(self.combat.player_pokemon, (50, 350))
        self.draw_hp_bar(self.combat.wild_pokemon, (250, 150))

        # ✅ Affichage des boutons
        self.draw_buttons()

        # ✅ Gestion de l'animation d'attaque
        if self.attack_animation:
            current_time = pygame.time.get_ticks()
            if current_time - self.animation_timer < 100:
                self.animation_offset = -5
            else:
                self.animation_offset = 0
                self.attack_animation = False

        pygame.display.flip()

    def draw_hp_bar(self, pokemon, position):
        """ Dessine une barre de vie pour le Pokémon """
        max_bar_width = 100
        bar_height = 10
        current_hp_ratio = max(0, pokemon.hp / pokemon.max_hp)
        current_bar_width = int(max_bar_width * current_hp_ratio)

        pygame.draw.rect(self.screen, (255, 0, 0), (position[0], position[1], max_bar_width, bar_height))  # Barre rouge
        pygame.draw.rect(self.screen, (0, 255, 0), (position[0], position[1], current_bar_width, bar_height))  # Barre verte
        hp_text = self.font.render(f"{pokemon.hp}/{pokemon.max_hp}", True, (255, 255, 255))
        self.screen.blit(hp_text, (position[0] + 40, position[1] - 15))

    def draw_buttons(self):
        """ Affiche les boutons d'attaque, fuite et capture """
        for action, rect in self.buttons.items():
            pygame.draw.rect(self.screen, (50, 50, 50), rect)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)

            text = self.button_font.render(action.capitalize(), True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def get_button_click(self, position):
        """ Vérifie si un bouton a été cliqué et retourne son action """
        for action, rect in self.buttons.items():
            if rect.collidepoint(position):
                return action
        return None

    def trigger_attack_animation(self):
        """ Active une animation d'attaque rapide """
        self.attack_animation = True
        self.animation_timer = pygame.time.get_ticks()
