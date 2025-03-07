import pygame

class TeamView:
    def __init__(self, controller):
        self.controller = controller
        self.screen = controller.view.screen
        self.font = pygame.font.Font(None, 24)
        self.visible = False  # visibilité initiale : cachée

    def render(self):
        # Ne pas faire pygame.display.flip() ici.
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Affiche Pokémon
        for idx, pokemon in enumerate(self.controller.player.pokemons):
            text = self.font.render(
                f"{pokemon.name} HP: {pokemon.hp}/{pokemon.max_hp}",
                True, (255, 255, 255))
            self.screen.blit(text, (50, 50 + 30 * idx))

           
            
        
   