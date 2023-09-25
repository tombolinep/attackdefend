import pygame


class HealthBarView:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, surface, x, y, health_ratio):
        pygame.draw.rect(surface, (255, 0, 0), (x, y, self.width, self.height))
        pygame.draw.rect(surface, (0, 255, 0), (x, y, self.width * health_ratio, self.height))
