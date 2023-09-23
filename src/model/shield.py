import pygame
from constants import WARP_FIELD_DIAMETER, SHIELD_DIAMETER
from controller.warpfield_controller import WarpFieldController
from view.warpfield_view import WarpFieldView


class Shield(pygame.sprite.Sprite):
    def __init__(self, game_model, player, image_manager):
        super().__init__()
        self.game_model = game_model
        self.player = player
        self.image_manager = image_manager

        self.x = 0
        self.y = 0
        self.diameter = SHIELD_DIAMETER

        self.screen = pygame.display.get_surface()
        self.image = image_manager.get_image('shield1')
        self.surf = pygame.Surface((SHIELD_DIAMETER, SHIELD_DIAMETER), pygame.SRCALPHA)
        self.rect = self.surf.get_rect()

        self.view = WarpFieldView(self)
        self.controller = WarpFieldController(self, self.view)

    def update_image(self):
        shield_level = self.player.attributes_bought.get('shield', 0)
        if shield_level > 0:
            self.image = self.image_manager.get_specific_shield_image(shield_level)
        else:
            self.image = None

    def update(self):
        self.surf.fill((0, 0, 0, 0))
        self.update_image()
        self.controller.update()
