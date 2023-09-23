import pygame


class WarpFieldView:
    def __init__(self, model):
        self.model = model

    def draw(self, screen):
        if self.model.game_model.player.attributes_bought.get('warp_field_enabled') == 1:
            # Blit the warp field image onto the transparent surface
            self.model.surf.blit(self.model.image, (0, 0))
        # Draw the surface onto the screen
        screen.blit(self.model.surf, self.model.rect.topleft)
