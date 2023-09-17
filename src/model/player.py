import math
from typing import Any

import pygame
from constants import PLAYER_DIAMETER, STATS_WIDTH, MAIN_GAME_WIDTH, SCREEN_HEIGHT, WARP_FIELD_DIAMETER
from model.bullet import Bullet


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
        self.coins = 1000
        self.attributes_bought = {key: 0 if isinstance(value, int) else value for key, value in
                                  self.ATTRIBUTE_DEFAULTS.items()}

        for attribute in self.ATTRIBUTE_DEFAULTS:
            setattr(self, attribute, self.ATTRIBUTE_DEFAULTS[attribute] + self.attributes_bought[attribute])

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
        current_value: int | Any = self.attributes_bought.get(attribute, 0)

        if action in ["buy", "increase"]:
            new_value = current_value + change_amount
        elif action in ["sell", "decrease"]:
            new_value = current_value - change_amount

        self.attributes_bought[attribute] = new_value
        setattr(self, attribute, self.ATTRIBUTE_DEFAULTS[attribute] + new_value)

    def get_effective_attribute(self, attribute):
        base_value = getattr(self, attribute, 0)
        modifier = self.attributes_bought.get(attribute, 0)
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
        current_value = self.attributes_bought.get(attribute, default_value)

        if current_value is None or default_value is None:
            return False
        if attribute == "diameter" or attribute == "reload_speed" or "num_of_guns":
            return current_value - decrease_amount >= 0
        if isinstance(default_value, (int, float)):
            return current_value - decrease_amount >= default_value
        if isinstance(default_value, bool):
            return current_value
        return False

    def sell_item(self, attribute, decrease_amount, item_price):
        if self.can_sell_item(attribute, decrease_amount):
            self.attributes_bought[attribute] -= decrease_amount
            setattr(self, attribute, self.attribute)
            self.coins += item_price
            return True
        return False

    def shoot(self):
        num_of_guns = self.num_of_guns
        bullets = []
        for i in range(num_of_guns):
            angle_offset = math.radians(i * 10 - (5 * (num_of_guns - 1)))

            new_bullet = Bullet(self.rect.centerx + (i * 20 - (10 * (num_of_guns - 1))),
                                self.rect.top + (i * 10 - (5 * (num_of_guns - 1))))

            new_bullet.adjust_trajectory(angle_offset)
            bullets.append(new_bullet)
        return bullets

    def update(self):
        self.center = (self.x + self.radius, self.y + self.radius)
        if self.view:
            self.view.update_shield()

    def is_point_in_warp_field(self, point):
        return ((self.x - point[0]) ** 2 + (self.y - point[1]) ** 2) ** 0.5 < (WARP_FIELD_DIAMETER / 2)
