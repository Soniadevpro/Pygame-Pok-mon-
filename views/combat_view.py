import pygame

class CombatView:
    def __init__(self, controller, combat):
        self.controller = controller
        self.combat = combat
        self.screen = controller.view.screen
        self.font = pygame.font.Font(None, 24)
        
        
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

        pygame.display.flip()
