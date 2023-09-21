import math

import pygame
from pygame.time import get_ticks
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH
from controller.rocket_controller import RocketController
from view.rocket_view import RocketView


class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, audio_manager, image_manager):
        super().__init__()
        self.audio_manager = audio_manager
        self.image_manager = image_manager

        self.rocket_image = self.image_manager.get_image('rocket')
        self.surf = pygame.transform.scale(self.image_manager.get_image('rocket'), (20, 20))
        self.explosion_image = self.image_manager.get_image('explosion')
        center_bottom_color = self.explosion_image.get_at(
            (self.explosion_image.get_width() // 2, self.explosion_image.get_height() - 1))
        self.explosion_image.set_colorkey(center_bottom_color)

        self.image = self.rocket_image
        self.surf = pygame.transform.scale(self.image, (20, 20))  # Adjust size as needed
        self.rect = self.surf.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.surf)

        self.speed = 5
        self.target_x = target_x
        self.target_y = target_y
        self.calculate_trajectory()
        self.start_time = get_ticks()
        self.explosion_time = 1500
        self.explosion_radius = 150
        self.is_exploding = False
        self.explosion_duration = 100

        self.screen = pygame.display.get_surface()

        self.view = RocketView(self)
        self.controller = RocketController(self, self.view)

    def calculate_trajectory(self):
        dx = self.target_x - self.rect.x
        dy = self.target_y - self.rect.y
        distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)
        self.dx = dx / distance
        self.dy = dy / distance

    def explode(self):
        self.is_exploding = True
        self.start_time = get_ticks()
        self.image = pygame.transform.scale(self.explosion_image, (20, 20))
        self.surf = self.image
        self.rect = self.surf.get_rect(center=self.rect.center)
        self.audio_manager.play_rocket_explosion()

    def is_out_of_bounds(self):
        return (self.rect.x < STATS_WIDTH or self.rect.y < 0 or
                self.rect.x > SCREEN_WIDTH or self.rect.y > SCREEN_HEIGHT)

    def update(self):
        self.controller.update()
        if self.is_exploding:
            current_time = get_ticks()
            elapsed_time = max(0, current_time - self.start_time)
            max_duration = self.explosion_duration

            max_size = self.explosion_radius * 2
            base_size = 0.5 * max_size  # Set the base size to 1% of the maximum size

            log_growth_factor = 10  # This value controls the growth rate; adjust as needed
            growth_rate = log_growth_factor * (math.log1p(elapsed_time))  # Applying logarithmic growth
            new_size = int(base_size + growth_rate * (max_size - base_size) / max_duration)

            # Cap the size to max_size
            new_size = min(new_size, max_size)

            self.image = pygame.transform.scale(self.explosion_image, (new_size, new_size))
            self.surf = self.image
            self.rect = self.surf.get_rect(center=self.rect.center)
