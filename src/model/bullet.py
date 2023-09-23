import math
import pygame

from constants import BULLET_SIZE
from view.bullet_view import BulletView


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, image_manager, settings):
        super().__init__()
        self.settings = settings
        self.image = image_manager.get_image('bullet')
        self.surf = pygame.transform.scale(self.image, (BULLET_SIZE, BULLET_SIZE))
        self.rect = self.surf.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.surf)
        self.radius = self.rect.width // 2

        self.speed = 5
        self.calculate_trajectory(target_x, target_y)
        self.view = BulletView(self)

    def calculate_trajectory(self, target_x, target_y):
        dx = target_x - self.rect.x
        dy = target_y - self.rect.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        self.dx = dx / distance
        self.dy = dy / distance

    def update(self):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        if self.is_out_of_bounds():
            self.kill()

    def is_out_of_bounds(self):
        return (self.rect.x < self.settings.STATS_WIDTH or self.rect.y < 0 or
                self.rect.x > self.settings.SCREEN_WIDTH or self.rect.y > self.settings.SCREEN_HEIGHT)

    def adjust_trajectory(self, angle_offset):
        angle = math.atan2(self.dy, self.dx)
        angle += math.radians(angle_offset)
        self.dx = math.cos(angle)
        self.dy = math.sin(angle)
