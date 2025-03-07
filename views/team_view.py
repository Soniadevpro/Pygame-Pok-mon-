import pygame

class TeamView:
    def __init__(self, controller):
        self.controller = controller
        self.screen = controller.view.screen
        self.font = pygame.font.Font(None, 24)
        self.visible = False
        
        
        
    def render(self):
        if not self.visible:
            return
        
        # Fond semi-transparent noir
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        
        for idx, pokemon in enumerate(self.controller.player.pokemons):
            pokemon_text = self.font.render(
                f"{pokemon.name} - Niveau : {pokemon.level} - HP : {pokemon.hp}/{pokemon.max_hp}",
                True, (255, 255, 255)
            )
            self.screen.blit(pokemon_text, (50, 50 + idx * 30))
           
            
        
   