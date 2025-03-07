import pygame

class CombatView:
    def __init__(self, controller, combat):
        self.controller = controller
        self.combat = combat
        self.screen = controller.view.screen
        self.font = pygame.font.Font(None, 24)
        
        # Définir clairement les boutons (Attaque, Fuite)
        self.attack_button = pygame.Rect(50, 500, 100, 40)
        self.run_button = pygame.Rect(200, 500, 100, 40)
        
        # button capture
        self.capture_button = pygame.Rect(350, 500, 120, 40)
        
        
        
    def render(self):
        self.screen.fill((30, 30, 30))
        

        # Pokémon du joueur
        player_pokemon_text = self.font.render(
            f"Votre Pokémon : {self.combat.player_pokemon.name} HP: {self.combat.player_pokemon.hp}/{self.combat.player_pokemon.max_hp}",
            True, (255, 255, 255)
        )
        self.screen.blit(player_pokemon_text, (50, 450))

        # Pokémon sauvage
        wild_pokemon_text = self.font.render(
            f"Sauvage : {self.combat.wild_pokemon.name} HP: {self.combat.wild_pokemon.hp}/{self.combat.wild_pokemon.max_hp}",
            True, (255, 255, 255)
        )
        self.screen.blit(wild_pokemon_text, (50, 50))
        
        
        # Draw buttons
        pygame.draw.rect(self.screen, (0, 200, 0), self.attack_button)
        pygame.draw.rect(self.screen, (200, 0, 0), self.run_button)
        
        
        # Draw text on buttons
        attack_text = self.font.render("Attaque", True, (255, 255, 255))
        run_text = self.font.render("Fuite", True, (255, 255, 255))
        
        #capture button
        pygame.draw.rect(self.screen, (0, 0, 200), self.capture_button)
        capture_text = self.font.render("Capture", True, (255, 255, 255))
        self.screen.blit(capture_text, (self.capture_button.x + 10, self.capture_button.y + 10))
        
        pygame.display.flip()

    def get_button_click(self, pos):
        if self.attack_button.collidepoint(pos):
            return "attack"
        elif self.run_button.collidepoint(pos):
            return "run"
        elif self.capture_button.collidepoint(pos):
            return "capture"
        return None