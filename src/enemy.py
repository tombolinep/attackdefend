import pygame
import random

from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH, MAIN_GAME_WIDTH
from src.player import Player


class Enemy(pygame.sprite.Sprite):
    def __init__(self, score, type="white"):
        super(Enemy, self).__init__()
        self.type = type
        self.surf = pygame.Surface((20, 10))
        if self.type == "red":
            self.surf.fill((255, 0, 0))  # Red color
        else:
            self.surf.fill((255, 255, 255))  # Default to white color

        base_speed = random.randint(1, 2)
        increment = score // 440  # Increase speed for every 100 points in the score
        adjusted_speed = base_speed + increment
        self.speed = min(adjusted_speed, 12)  # Adjust the maximum speed here

        # Choose a side from which the enemy should spawn: 0 = top, 1 = right, 2 = bottom, 3 = left
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

        self.initial_speed = self.speed
        self.speedup_timer = pygame.time.get_ticks()

    def update(self, player_center=None):
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
        if (self.rect.right < STATS_WIDTH or self.rect.left > STATS_WIDTH + MAIN_GAME_WIDTH or
                self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()
