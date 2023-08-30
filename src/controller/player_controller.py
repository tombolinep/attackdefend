import pygame

from src.constants import STATS_WIDTH, SCREEN_HEIGHT, SCREEN_WIDTH, MAIN_GAME_WIDTH


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
        self.model.x = self.model.rect.x
        self.model.y = self.model.rect.y

    def _keep_within_boundaries(self):
        self.model.rect.x = max(self.model.rect.x, STATS_WIDTH)
        self.model.rect.x = min(self.model.rect.x, STATS_WIDTH + MAIN_GAME_WIDTH - self.model.rect.width)
        self.model.rect.y = max(self.model.rect.y, 0)
        self.model.rect.y = min(self.model.rect.y, SCREEN_HEIGHT - self.model.rect.height)
