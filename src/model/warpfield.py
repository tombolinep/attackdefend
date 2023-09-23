from math import sqrt

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
        self.image.set_alpha(76)

        original_width, original_height = self.image.get_size()
        diagonal_length = int(sqrt(original_width ** 2 + original_height ** 2))

        self.surf = pygame.Surface((diagonal_length, diagonal_length), pygame.SRCALPHA)
        self.rect = self.surf.get_rect()
        self.surf = pygame.Surface((WARP_FIELD_DIAMETER, WARP_FIELD_DIAMETER), pygame.SRCALPHA)
        self.rect = self.surf.get_rect()

        self.view = WarpFieldView(self)
        self.controller = WarpFieldController(self, self.view)

    def update(self):
        self.surf.fill((0, 0, 0, 0))
        self.controller.update()
