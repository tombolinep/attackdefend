from typing import Any

import pygame
from src.constants import PLAYER_DIAMETER, STATS_WIDTH, MAIN_GAME_WIDTH, SCREEN_HEIGHT
from src.model.bullet import Bullet


class Player(pygame.sprite.Sprite):
    ATTRIBUTE_DEFAULTS = {
        'speed': 7,
        'shield': 0,
        'reload_speed': 1,
        'diameter': PLAYER_DIAMETER,
        'tractor_beam_enabled': False,
        'warp_field_enabled': False,
        'num_of_guns': 1,
        'rocket_launcher_enabled': False,
        'laser_enabled': False
    }

    def __init__(self, view=None):
        super().__init__()
        self.view = view
        self.color = (0, 0, 255)
        self.coins = 100
        self.attribute_modifiers = {key: 0 if isinstance(value, int) else value for key, value in
                                    self.ATTRIBUTE_DEFAULTS.items()}

        for attribute in self.ATTRIBUTE_DEFAULTS:
            setattr(self, attribute, self.ATTRIBUTE_DEFAULTS[attribute] + self.attribute_modifiers[attribute])

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

    def update_attribute(self, attribute, change_amount, action):
        current_value: int | Any = self.attribute_modifiers.get(attribute, 0)

        if action in ["buy", "increase"]:
            new_value = current_value + change_amount
        elif action in ["sell", "decrease"]:
            new_value = current_value - change_amount

        self.attribute_modifiers[attribute] = new_value
        setattr(self, attribute, self.ATTRIBUTE_DEFAULTS[attribute] + new_value)

    def get_effective_attribute(self, attribute):
        base_value = getattr(self, attribute, 0)
        modifier = self.attribute_modifiers.get(attribute, 0)
        return base_value + modifier

    def purchase_item(self, price):
        if self.coins >= price:
            self.coins -= price
            return True
        return False

    def can_sell_item(self, attribute, decrease_amount):
        if not attribute:
            return False

        default_value = self.ATTRIBUTE_DEFAULTS.get(attribute)
        current_value = getattr(self, attribute, None)
        if current_value is None or default_value is None:
            return False
        if isinstance(default_value, int):
            return current_value - decrease_amount >= default_value
        if isinstance(default_value, bool):
            return current_value == True
        return False

    def sell_item(self, attribute, decrease_amount, item_price):
        if self.can_sell_item(attribute, decrease_amount):
            self.attribute_modifiers[attribute] -= decrease_amount
            setattr(self, attribute, self.get_effective_attribute(attribute))
            self.coins += item_price
            return True
        return False

    def shoot(self):
        new_bullet = Bullet(self.rect.centerx, self.rect.top)
        return new_bullet

    def update(self):
        self.center = (self.x + self.radius, self.y + self.radius)
        if self.view:
            self.view.update_shield()
