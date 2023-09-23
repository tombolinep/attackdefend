import pygame


class WarpFieldView:
    def __init__(self, model):
        self.model = model
        self.model.surf = pygame.Surface((self.model.image.get_width(), self.model.image.get_height()), pygame.SRCALPHA)
        self.model.surf.blit(self.model.image, (0, 0))

    def draw(self, screen):
        if self.model.game_model.player.attributes_bought.get('warp_field_enabled') == 1:
            self.model.rect.center = (self.model.player.rect.centerx, self.model.player.rect.centery)
            screen.blit(self.model.surf, self.model.rect.topleft)
