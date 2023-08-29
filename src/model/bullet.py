import pygame
import math
from src.utils import resource_path

from src.constants import SCREEN_HEIGHT


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target):
        super().__init__()

        self.surf = pygame.Surface((10, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(topleft=(x, y))
        image_path = resource_path('../assets/overhead.png')
        self.surf = pygame.image.load(image_path).convert_alpha()

        self.speed = 5
        self.calculate_trajectory(target)

    def calculate_trajectory(self, target):
        dx = target.rect.centerx - self.rect.centerx
        dy = target.rect.centery - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        self.dx = dx / distance
        self.dy = dy / distance

    def update(self):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
