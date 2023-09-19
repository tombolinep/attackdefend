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

        self.screen = pygame.display.get_surface()
        self.image = image_manager.get_image('tractor_beam')
        self.surf = pygame.Surface((100, 200), pygame.SRCALPHA)  # Changed to a transparent surface
        self.rect = self.surf.get_rect()
        self.mask = pygame.mask.from_surface(self.surf)

        self.view = TractorBeamView(self)
        self.controller = TractorBeamController(self, self.view)

    def update(self):
        self.surf.fill((0, 0, 0, 0))  # Clear the surface at the start of each frame
        self.controller.update()
