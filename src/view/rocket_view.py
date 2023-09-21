import pygame


class RocketView:
    def __init__(self, model):
        self.model = model

    def draw(self, screen):
        if not self.model.is_exploding:
            screen.blit(self.model.surf, self.model.rect.topleft)
        else:
            screen.blit(self.model.surf, self.model.rect.topleft)
