import pygame

from controller.tractor_beam_controller import TractorBeamController
from view.tractor_beam_view import TractorBeamView


class TractorBeam(pygame.sprite.Sprite):
    def __init__(self, game_model, player, image_manager):
        super().__init__()
        self.game_model = game_model
        self.player = player
        self.range = 300
        self.pull_strength = 1
        self.image = image_manager.get_image('tractor_beam')
        self.surf = pygame.transform.scale(self.image, (100, 100))  # Adjust size as necessary
        self.rect = self.surf.get_rect()
        self.mask = pygame.mask.from_surface(self.surf)

        self.view = TractorBeamView(self)
        self.controller = TractorBeamController(self, self.view)

    def update(self, screen):
        self.controller.update(screen)
