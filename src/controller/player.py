import pygame

from src.constants import STATS_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH


class PlayerController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update(self, pressed_keys):
        self._handle_movement(pressed_keys)
        self._keep_within_boundaries()

    def _handle_movement(self, pressed_keys):
        if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]:
            self.model.rect.move_ip(0, -self.model.speed)
        if pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
            self.model.rect.move_ip(0, self.model.speed)
        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
            self.model.rect.move_ip(-self.model.speed, 0)
        if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
            self.model.rect.move_ip(self.model.speed, 0)

    def _keep_within_boundaries(self):
        self.model.rect.left = max(self.model.rect.left, STATS_WIDTH)
        self.model.rect.right = min(self.model.rect.right, SCREEN_WIDTH)
        self.model.rect.top = max(self.model.rect.top, 0)
        self.model.rect.bottom = min(self.model.rect.bottom, SCREEN_HEIGHT)

    def update(self, pressed_keys):
        self._handle_movement(pressed_keys)
        self._keep_within_boundaries()
