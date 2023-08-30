import pygame
from src.constants import PLAYER_DIAMETER, STATS_WIDTH, MAIN_GAME_WIDTH, SCREEN_HEIGHT
from src.model.bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, view=None):
        super().__init__()
        self.view = view
        self.color = (0, 0, 255)
        self.speed = 7
        self.coins = 0
        self.shield = 0
        self.diameter = PLAYER_DIAMETER
        self.x = STATS_WIDTH + MAIN_GAME_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.radius = self.diameter // 2
        self.center = (self.x + self.radius, self.y + self.radius)

    def add_coin(self, amount=1):
        self.coins += amount

    def deduct_coin(self, amount):
        if self.coins >= amount:
            self.coins -= amount
            return True
        return False

    def increase_speed(self, increment=2):
        self.speed += increment

    def add_shield(self):
        self.shield += 1

    def remove_shield(self):
        if self.shield > 0:
            self.shield -= 1

    def get_shield(self):
        return self.shield

    def purchase_item(self, price):
        if self.coins >= price:
            self.coins -= price
            return True
        return False

    def shoot(self):
        new_bullet = Bullet(self.rect.centerx, self.rect.top)
        return new_bullet

    def update(self):
        self.center = (self.x + self.radius, self.y + self.radius)
        if self.view:
            self.view.update_shield()
