import math
import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((255, 0, 0))  # Fill it with red color
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.calculate_trajectory(target_x, target_y)

    def calculate_trajectory(self, target_x, target_y):
        dx = target_x - self.rect.x
        dy = target_y - self.rect.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        self.dx = dx / distance
        self.dy = dy / distance

    def update(self):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
