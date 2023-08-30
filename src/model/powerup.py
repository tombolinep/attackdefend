import pygame

from src.constants import POWERUP_SIZE


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

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
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_color_change_time >= self.color_change_interval:
            self.last_color_change_time = current_time
            self.current_color_index = (self.current_color_index + 1) % len(self.colors)
            self.surf = self.create_surface_with_color()

    def create_surface_with_color(self):
        color = self.colors[self.current_color_index]
        surf = pygame.Surface((POWERUP_SIZE, POWERUP_SIZE), pygame.SRCALPHA)

        # Define star points relative to the size of the PowerUp
        star_points = [
            (0.5, 0.0),
            (0.7, 0.35),
            (1.0, 0.4),
            (0.8, 0.7),
            (0.9, 1.0),
            (0.5, 0.8),
            (0.1, 1.0),
            (0.2, 0.7),
            (0.0, 0.4),
            (0.3, 0.35)
        ]

        scaled_points = [(int(x * POWERUP_SIZE), int(y * POWERUP_SIZE)) for x, y in star_points]

        pygame.draw.polygon(surf, color, scaled_points)

        return surf

    def apply_powerup(self, enemies_group):
        white_enemies = [enemy for enemy in enemies_group if enemy.type == "white"]
        for enemy in white_enemies:
            enemy.kill()
