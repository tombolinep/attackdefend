import math

import pygame


class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.speed = 5
        self.calculate_trajectory(target_x, target_y)

    def calculate_trajectory(self, target_x, target_y):
        dx = target_x - self.rect.x
        dy = target_y - self.rect.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        self.dx = dx / distance
        self.dy = dy / distance
