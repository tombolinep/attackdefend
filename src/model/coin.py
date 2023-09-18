import pygame

from constants import COIN_SIZE
from view.coin_view import CoinView


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y

        self.image = pygame.image.load('assets/coin.png').convert_alpha()
        self.surf = pygame.transform.scale(self.image, (COIN_SIZE, COIN_SIZE))
        self.rect = self.surf.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.surf)
        self.radius = self.rect.width / 2

        self.view = CoinView(self)
