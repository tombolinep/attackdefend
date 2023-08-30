import pygame
import random
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH
from src.model.player import Player


class Enemy(pygame.sprite.Sprite):
    def __init__(self, score, enemy_type="white"):
        super().__init__()
        self.type = enemy_type
        self.surf = pygame.Surface((20, 10))
        if self.type == "red":
            self.surf.fill((255, 0, 0))  # Red color
        else:
            self.surf.fill((255, 255, 255))  # Default to white color

        self.base_speed = random.randint(1, 2)
        self.adjusted_speed = self.base_speed + score // 440
        self.speed = min(self.adjusted_speed, 12)

        self.initial_position()
        self.speedup_timer = pygame.time.get_ticks()

    def initial_position(self):
        side = random.randint(0, 3)
        if side == 0:  # top
            self.rect = self.surf.get_rect(center=(random.randint(STATS_WIDTH, SCREEN_WIDTH), -10))
            self.dx, self.dy = 0, self.speed
        elif side == 1:  # right
            self.rect = self.surf.get_rect(center=(SCREEN_WIDTH + 10, random.randint(0, SCREEN_HEIGHT)))
            self.dx, self.dy = -self.speed, 0
        elif side == 2:  # bottom
            self.rect = self.surf.get_rect(center=(random.randint(STATS_WIDTH, SCREEN_WIDTH), SCREEN_HEIGHT + 10))
            self.dx, self.dy = 0, -self.speed
        else:  # left
            self.rect = self.surf.get_rect(center=(STATS_WIDTH - 10, random.randint(0, SCREEN_HEIGHT)))
            self.dx, self.dy = self.speed, 0

    def update_position(self, player_center=None):
        if self.type == "red" and player_center:
            shield_space = len(Player.SHIELD_COLORS) * 5
            adjusted_player_center = (player_center[0] + shield_space, player_center[1] + shield_space)

            dx = adjusted_player_center[0] - self.rect.centerx
            dy = adjusted_player_center[1] - self.rect.centery

            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance > 0:
                dx /= distance
                dy /= distance

            if distance < self.speed:
                self.rect.center = adjusted_player_center
            else:
                self.rect.x += dx * self.speed
                self.rect.y += dy * self.speed
        else:
            self.rect.move_ip(self.dx, self.dy)
        if (self.rect.right < STATS_WIDTH or self.rect.left > SCREEN_WIDTH or
                self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()
