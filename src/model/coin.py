from random import choice, sample
import pygame
from constants import COIN_SIZE
from view.coin_view import CoinView


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, image_manager):
        super().__init__()

        self.image = image_manager.get_random_coin_image()
        self.surf = pygame.transform.scale(self.image, (COIN_SIZE, COIN_SIZE))
        self.rect = self.surf.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.surf)
        self.radius = self.rect.width / 2

        self.view = CoinView(self)
