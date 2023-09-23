import pygame


class WarpFieldView:
    def __init__(self, model):
        self.model = model
        self.angle = 0

    def draw(self, screen):
        if self.model.game_model.player.attributes_bought.get('warp_field_enabled') == 1:
            self.angle = (self.angle + 1) % 360
            rotated_image = pygame.transform.rotate(self.model.game_model.image_manager.get_image('warp_field'),
                                                    self.angle)
            new_rect = rotated_image.get_rect(center=self.model.surf.get_rect().center)
            self.model.surf.blit(rotated_image, new_rect.topleft)
            screen.blit(self.model.surf, self.model.rect.topleft)
