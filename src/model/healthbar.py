import pygame

from controller.healthbar_controller import HealthBarController
from view.healthbar_view import HealthBarView


class HealthBarModel(pygame.sprite.Sprite):
    def __init__(self, enemy):
        super().__init__()

        self.enemy = enemy

        self.current_health = enemy.health
        self.max_health = enemy.max_health
        self.screen = pygame.display.get_surface()

        self.width = 50
        self.height = 5

        self.surf = pygame.Surface((self.width, self.height))
        self.rect = self.surf.get_rect()

        enemy_x, enemy_y = enemy.rect.x, enemy.rect.bottom
        self.rect.topleft = (enemy_x, enemy_y + 5)

        self.view = HealthBarView(self.width, self.height)
        self.controller = HealthBarController(self, self.view)

    def set_health(self, health):
        self.current_health = max(0, min(self.max_health, health))

    def get_health_ratio(self):
        return self.current_health / self.max_health

    def update(self):
        self.rect.topleft = (self.enemy.rect.x, self.enemy.rect.bottom + 5)
        self.controller.update(self.screen)
