import pygame


class EnemyView:
    def __init__(self, model):
        self.model = model

    def draw(self, screen):
        screen.blit(self.model.surf, self.model.rect.topleft)
