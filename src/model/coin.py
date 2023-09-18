from random import choice, sample
import pygame
from constants import COIN_SIZE
from view.coin_view import CoinView

COIN_IMAGE = pygame.image.load('assets/coin.png')
COIN_ROTATIONS = [pygame.transform.rotate(COIN_IMAGE, i) for i in sample(range(0, 360), 5)]


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = choice(COIN_ROTATIONS)
        self.surf = pygame.transform.scale(self.image, (COIN_SIZE, COIN_SIZE))
        self.rect = self.surf.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.surf)
        self.radius = self.rect.width / 2

        self.view = CoinView(self)
