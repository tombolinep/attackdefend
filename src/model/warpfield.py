import pygame
from constants import WARP_FIELD_DIAMETER
from controller.warpfield_controller import WarpFieldController
from view.warpfield_view import WarpFieldView


class WarpField(pygame.sprite.Sprite):
    def __init__(self, game_model, player, image_manager):
        super().__init__()
        self.game_model = game_model
        self.player = player

        self.x = 0
        self.y = 0
        self.diameter = WARP_FIELD_DIAMETER

        self.screen = pygame.display.get_surface()
        self.image = image_manager.get_image('warp_field')
        self.image = pygame.transform.scale(self.image, (self.diameter, self.diameter))
        self.rect = self.image.get_rect(center=(self.x, self.y))


        self.view = WarpFieldView(self)
        self.controller = WarpFieldController(self, self.view)

    def update(self):
        if self.game_model.player.attributes_bought.get('warp_field_enabled') == 1:
            self.rect.center = (self.player.rect.centerx, self.player.rect.centery)
            self.controller.update()
