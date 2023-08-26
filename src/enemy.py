import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH, MAIN_GAME_WIDTH


class Enemy(pygame.sprite.Sprite):
    def __init__(self, score, type="white"):
        super(Enemy, self).__init__()
        self.type = type
        self.surf = pygame.Surface((20, 10))

        if self.type == "yellow":
            self.surf.fill((255, 255, 0))  # Yellow color
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

    def update(self):
        self.rect.move_ip(self.dx, self.dy)

        # Kill the sprite if it's out of the screen to avoid unnecessary processing
        if (self.rect.right < STATS_WIDTH or self.rect.left > SCREEN_WIDTH or
                self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()
