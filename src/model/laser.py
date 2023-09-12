import pygame
import math
from pygame.time import get_ticks

from src.constants import STATS_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, audio_manager):
        super().__init__()
        self.audio_manager = audio_manager
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y

        self.color = (255, 0, 0)
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        self.length = max(1, (dx ** 2 + dy ** 2) ** 0.5)

        self.angle = math.degrees(math.atan2(dy, dx))
        self.start_time = get_ticks()
        self.duration = 500

    def update(self):
        print("update laser")
        current_time = get_ticks()
        if current_time - self.start_time >= self.duration:
            return True

    def is_out_of_bounds(self):
        rect = self.get_rect()
        return (rect.x < STATS_WIDTH or rect.y < 0 or
                rect.x > SCREEN_WIDTH or rect.y > SCREEN_HEIGHT)

    def draw(self, screen):
        image = pygame.Surface((self.length, 5), pygame.SRCALPHA)
        image.fill(self.color)

        image = pygame.transform.rotate(image, -self.angle)
        rect = image.get_rect(center=(self.x, self.y))

        screen.blit(image, rect)
