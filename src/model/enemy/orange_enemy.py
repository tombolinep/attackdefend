import math

import pygame

from constants import ENEMY_WIDTH, ENEMY_HEIGHT
from model.enemy.enemy import EnemyBase


class OrangeEnemy(EnemyBase):
    def __init__(self, score, player, image_manager, settings):
        super().__init__(score, player, image_manager, settings)
        self.type = "orange"
        self.steps = 0
        self.max_steps = 50  # Number of steps for one full circle
        self.dx_dy_cache = self.generate_cache()

    def generate_cache(self):
        cache = []
        for step in range(self.max_steps):
            angle = 2 * math.pi * step / self.max_steps
            dx = math.cos(angle) * 4  # adjust multiplier for speed
            dy = math.sin(angle) * 6  # adjust multiplier for speed
            cache.append((dx, dy))
        return cache

    def set_image(self, image_manager):
        raw_surf = image_manager.get_image('enemy_orange')
        self.surf = pygame.transform.scale(raw_surf, (ENEMY_WIDTH, ENEMY_HEIGHT))
        self.rect = self.surf.get_rect()
        self.mask = pygame.mask.from_surface(self.surf)
        self.radius = self.rect.width / 2

    def update_position(self):
        dx, dy = self.dx_dy_cache[self.steps]
        self.move(dx, dy, 1.0)

        self.steps = (self.steps + 1) % self.max_steps

        if self.rect.right < self.settings.STATS_WIDTH:
            self.kill()
