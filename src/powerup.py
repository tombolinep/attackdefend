import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super(PowerUp, self).__init__()

        self.width = 50
        self.height = 50
        self.colors = [
            (255, 0, 0),  # Red
            (0, 255, 0),  # Green
            (0, 0, 255),  # Blue
            (255, 255, 0),  # Yellow
            (0, 255, 255),  # Cyan
            (255, 0, 255)  # Magenta
        ]

        self.current_color_index = 0
        self.color_change_interval = 300  # Color change interval in milliseconds (0.3 seconds)
        self.last_color_change_time = pygame.time.get_ticks()

        self.surf = self.create_surface_with_color()

        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    def create_surface_with_color(self):
        color = self.colors[self.current_color_index]
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Draw a star-like shape using lines
        pygame.draw.line(surf, color, (self.width // 2, 0), (self.width // 2, self.height), 3)
        pygame.draw.line(surf, color, (0, self.height // 2), (self.width, self.height // 2), 3)
        pygame.draw.line(surf, color, (0, 0), (self.width, self.height), 3)
        pygame.draw.line(surf, color, (0, self.height), (self.width, 0), 3)

        return surf

    def update_color(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_color_change_time >= self.color_change_interval:
            self.last_color_change_time = current_time
            self.current_color_index = (self.current_color_index + 1) % len(self.colors)
            self.surf = self.create_surface_with_color()

    def apply_powerup(self, enemies_group):
        for enemy in enemies_group:
            enemy.kill()  # Remove all enemies from the group

    def update(self):
        self.update_color()
