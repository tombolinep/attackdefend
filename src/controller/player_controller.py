import pygame
from src.constants import STATS_WIDTH, SCREEN_HEIGHT, MAIN_GAME_WIDTH


class PlayerController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update(self, pressed_keys):
        self._handle_movement(pressed_keys)
        self._keep_within_boundaries()
        self.model.update()  # Make sure to update the model to calculate the new center

    def _handle_movement(self, pressed_keys):
        dx, dy = 0, 0
        if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]:
            dy = -self.model.speed
        if pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
            dy = self.model.speed
        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
            dx = -self.model.speed
        if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
            dx = self.model.speed

        # Update x and y in the model
        self.model.x += dx
        self.model.y += dy

    def _keep_within_boundaries(self):
        half_diameter = self.model.diameter / 2

        self.model.x = max(self.model.x, STATS_WIDTH + half_diameter)
        self.model.x = min(self.model.x, STATS_WIDTH + MAIN_GAME_WIDTH - half_diameter)
        self.model.y = max(self.model.y, half_diameter)
        self.model.y = min(self.model.y, SCREEN_HEIGHT - half_diameter)
