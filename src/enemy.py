import pygame
import random
import math

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH, MAIN_GAME_WIDTH


class Enemy(pygame.sprite.Sprite):
    def __init__(self, score, type="white"):
        super(Enemy, self).__init__()
        self.type = type
        self.surf = pygame.Surface((20, 10))
        if self.type == "yellow":
            self.surf.fill((255, 255, 0))  # Yellow color
        elif self.type == "red":
            self.surf.fill((255, 0, 0))  # Red color
        else:
            self.surf.fill((255, 255, 255))  # Default to white color

        base_speed = random.randint(1, 5)
        adjusted_speed = base_speed + 0.01 * score
        self.speed = min(adjusted_speed, 10)

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

        self.speedup_temporarily = False
        self.initial_speed = self.speed
        self.speedup_timer = pygame.time.get_ticks()

    def speed_up_temporarily(self):
        self.speedup_temporarily = True
        self.speed = self.initial_speed * 2
        self.speedup_timer = pygame.time.get_ticks()

    def update(self):
        if self.speedup_temporarily:
            if pygame.time.get_ticks() - self.speedup_timer >= 30000:  # 30 seconds
                self.speedup_temporarily = False
                self.speed = self.initial_speed
        self.rect.move_ip(self.dx, self.dy)

        # Kill the sprite if it's out of the main game screen area to avoid unnecessary processing
        if (self.rect.right < STATS_WIDTH or self.rect.left > STATS_WIDTH + MAIN_GAME_WIDTH or
                self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()
