import pygame

from src.utils import resource_path


class BulletView:
    def __init__(self, model):
        self.model = model
        image_path = resource_path('../assets/overhead.png')
        self.surf = pygame.image.load(image_path).convert_alpha()

    def draw(self, screen):
        screen.blit(self.surf, self.model.rect.topleft)
