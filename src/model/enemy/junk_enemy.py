import pygame

from constants import JUNK_HEIGHT, JUNK_WIDTH
from model.enemy.enemy import EnemyBase


class WhiteEnemy(EnemyBase):
    def __init__(self, score, player, image_manager, settings):
        super().__init__(score, player, image_manager, settings)
        self.type = "white"

    def set_image(self, image_manager):
        raw_surf = image_manager.get_random_junk_image()
        self.surf = pygame.transform.scale(raw_surf, (JUNK_WIDTH, JUNK_HEIGHT))
        self.rect = self.surf.get_rect()
        self.mask = pygame.mask.from_surface(self.surf)
        self.radius = self.rect.width / 2
