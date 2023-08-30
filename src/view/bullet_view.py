import pygame

from src.utils import resource_path


class BulletView:
    def __init__(self, model):
        self.model = model

    def draw(self, screen):
        screen.blit(self.model.image, self.model.rect.topleft)
