import pygame
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Enemy(pygame.sprite.Sprite):
    def __init__(self, score):
        super(Enemy, self).__init__()

        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))

        base_speed = random.randint(1, 5)
        adjusted_speed = base_speed + 0.01 * score
        self.speed = min(adjusted_speed, 10)

        # Choose a side from which the enemy should spawn: 0 = top, 1 = right, 2 = bottom, 3 = left
        side = random.randint(0, 3)

        if side == 0:  # top
            self.rect = self.surf.get_rect(center=(random.randint(0, SCREEN_WIDTH), -10))
            self.dx, self.dy = 0, self.speed
        elif side == 1:  # right
            self.rect = self.surf.get_rect(center=(SCREEN_WIDTH + 10, random.randint(0, SCREEN_HEIGHT)))
            self.dx, self.dy = -self.speed, 0
        elif side == 2:  # bottom
            self.rect = self.surf.get_rect(center=(random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT + 10))
            self.dx, self.dy = 0, -self.speed
        else:  # left
            self.rect = self.surf.get_rect(center=(-10, random.randint(0, SCREEN_HEIGHT)))
            self.dx, self.dy = self.speed, 0

    def update(self):
        self.rect.move_ip(self.dx, self.dy)

        # Kill the sprite if it's out of the screen to avoid unnecessary processing
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
                self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()
