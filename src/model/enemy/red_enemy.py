import pygame

from constants import ENEMY_WIDTH, ENEMY_HEIGHT
from model.enemy.enemy import EnemyBase


class RedEnemy(EnemyBase):
    def __init__(self, score, player, image_manager, settings):
        super().__init__(score, player, image_manager, settings)
        self.type = "red"

    def set_image(self, image_manager):
        raw_surf = image_manager.get_image('enemy_red')
        self.surf = pygame.transform.scale(raw_surf, (ENEMY_WIDTH, ENEMY_HEIGHT))
        self.rect = self.surf.get_rect()
        self.mask = pygame.mask.from_surface(self.surf)
        self.radius = self.rect.width / 2

    def update_position(self):
        slowdown_factor = 0.8 if self.in_warp_field else 1.0
        dx, dy = self.get_direction_towards_player()
        self.move(dx, dy, slowdown_factor)
        if self.rect.right < self.settings.STATS_WIDTH:
            self.kill()