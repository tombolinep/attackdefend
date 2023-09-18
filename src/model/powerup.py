import pygame

from constants import POWERUP_SIZE
from view.powerup_view import PowerUpView


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y

        self.image = pygame.image.load('assets/powerup.png').convert_alpha()
        self.surf = pygame.transform.scale(self.image, (POWERUP_SIZE, POWERUP_SIZE))
        self.rect = self.surf.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.surf)
        self.radius = self.rect.width / 2

        self.view = PowerUpView(self)
