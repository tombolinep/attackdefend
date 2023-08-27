import pygame
import random
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH, MAIN_GAME_WIDTH


class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super(PowerUp, self).__init__()

        self.nice_text = None

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
        self.color_change_interval = 300
        self.last_color_change_time = pygame.time.get_ticks()

        self.surf = self.create_surface_with_color()

        main_game_rect = pygame.Rect(STATS_WIDTH, 0, MAIN_GAME_WIDTH, SCREEN_HEIGHT)
        random_x = random.randrange(main_game_rect.left + self.width // 2, main_game_rect.right - self.width // 2)
        random_y = random.randrange(main_game_rect.top + self.height // 2, main_game_rect.bottom - self.height // 2)
        self.rect = self.surf.get_rect(center=(random_x, random_y))

    def create_surface_with_color(self):
        color = self.colors[self.current_color_index]
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

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
        white_enemies = [enemy for enemy in enemies_group if enemy.type == "white"]
        for enemy in white_enemies:
            enemy.kill()  # Remove all white enemies from the group
        self.set_nice_text("Nice!")

    def update(self):
        self.update_color()

    def set_nice_text(self, text):
        self.nice_text = text
