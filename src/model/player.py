import math
from typing import Any, Union

import pygame
from constants import PLAYER_SIZE


class Player(pygame.sprite.Sprite):
    ATTRIBUTE_DEFAULTS = {
        'speed': 7,
        'shield': 0,
        'reload_speed': 1,
        'size': PLAYER_SIZE,
        'tractor_beam_enabled': False,
        'warp_field_enabled': False,
        'num_of_guns': 1,
        'rocket_launcher_enabled': False,
        'laser_enabled': False
    }

    def __init__(self, image_manager, settings, view=None):
        super().__init__()
        self.settings = settings
        self.image_manager = image_manager
        self.view = view
        self.color = (0, 0, 255)
        self.coins = 0
        self.attributes_bought = {key: 0 if isinstance(value, int) else value for key, value in
                                  self.ATTRIBUTE_DEFAULTS.items()}

        for attribute in self.ATTRIBUTE_DEFAULTS:
            setattr(self, attribute, self.ATTRIBUTE_DEFAULTS[attribute] + self.attributes_bought[attribute])

        self.x = self.settings.STATS_WIDTH + self.settings.MAIN_GAME_WIDTH // 2
        self.y = self.settings.SCREEN_HEIGHT // 2
        self.image = image_manager.get_image('player')
        self.image = pygame.transform.scale(self.image, (PLAYER_SIZE, PLAYER_SIZE))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.image)
        self.radius = self.rect.width / 2
        self.original_image = self.image

    def add_coin(self, amount=1):
        self.coins += amount

    def update_attribute(self, attribute: str, change_amount: Union[int, bool], action: str):
        default_value = self.ATTRIBUTE_DEFAULTS.get(attribute)
        current_value = self.attributes_bought.get(attribute, default_value)

        if isinstance(default_value, int):
            if action == "increase":
                new_value = current_value + change_amount
            elif action == "decrease":
                new_value = current_value - change_amount
            else:
                raise ValueError("Invalid action for integer attribute")
        elif isinstance(default_value, bool):
            new_value = not current_value

        self.attributes_bought[attribute] = new_value
        setattr(self, attribute, self.ATTRIBUTE_DEFAULTS[attribute] + new_value) if isinstance(new_value,
                                                                                               int) else setattr(self,
                                                                                                                 attribute,
                                                                                                                 new_value)

        if attribute == 'size':
            self.update_sprite_size()

    def can_sell_item(self, attribute, decrease_amount):
        default_value = self.ATTRIBUTE_DEFAULTS.get(attribute)
        current_value = self.attributes_bought.get(attribute, default_value)

        if attribute in {"speed", "size", "reload_speed", "num_of_guns"}:
            return current_value - decrease_amount >= 0
        if isinstance(default_value, (int, float)):
            return current_value - decrease_amount >= default_value
        if isinstance(default_value, bool):
            return current_value
        return False

    def update(self):
        self.rect.center = (self.x, self.y)

    def update_sprite_size(self):
        new_value = self.size
        scale_factor = new_value / self.ATTRIBUTE_DEFAULTS['size']
        new_width = int(self.original_image.get_width() * scale_factor)
        new_height = int(self.original_image.get_height() * scale_factor)

        # Save the old center
        old_center = self.rect.center

        # Set the new image
        self.image = pygame.transform.scale(self.original_image, (new_width, new_height))

        # Set the new rect size
        self.rect.size = self.image.get_size()

        # Update the mask
        self.mask = pygame.mask.from_surface(self.image)

        # Set the rect center back to the old center
        self.rect.center = old_center
