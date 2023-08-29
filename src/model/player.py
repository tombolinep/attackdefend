import pygame
from pygame import Rect
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH, MAIN_GAME_WIDTH
from src.model.bullet import Bullet


class Player(pygame.sprite.Sprite):
    def __init__(self, view=None):
        super().__init__()
        self.view = view
        self.speed = 7
        self.coins = 0
        self.shield = 0
        # Create a basic sprite
        self.image = pygame.Surface([50, 50])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()

    def add_coin(self, amount=1):
        self.coins += amount

    def deduct_coin(self, amount):
        if self.coins >= amount:
            self.coins -= amount
            return True
        return False

    def increase_speed(self, increment=2):  # Increment can be adjusted based on your game's needs
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
        if self.view:
            self.view.update_shield()