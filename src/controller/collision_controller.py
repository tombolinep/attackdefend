import math
import random

import pygame
import pygame.gfxdraw

from constants import ENEMY_COIN_CHANCE


class CollisionController:
    def __init__(self, model, screen):
        self.model = model
        self.player = model.player
        self.enemies = model.enemies
        self.powerups = model.powerups
        self.coins = model.coins
        self.bullets = model.bullets
        self.rockets = model.rockets
        self.lasers = model.lasers
        self.audio_manager = model.audio_manager
        self.screen = screen
        self.running = model.running

    def is_circle_collision(obj1, obj2):
        dx = obj1.rect.centerx - obj2.rect.centerx
        dy = obj1.rect.centery - obj2.rect.centery
        distance = math.sqrt(dx * dx + dy * dy)
        return distance < (obj1.radius + obj2.radius)

    def handle_enemy_collision(self, enemy):
        if self.player.shield > 0:
            self.audio_manager.play_shield_hit_sound()
            self.player.update_attribute(attribute='shield', action='decrease', change_amount=1)
            if random.random() < ENEMY_COIN_CHANCE:
                self.model.spawn_coin_at_location(enemy.rect.x, enemy.rect.y)
            enemy.kill()
            self.model.score += 50
        else:
            self.audio_manager.play_death_sound()
            self.model.set_game_over(True)

    def handle_coin_collision(self, coin):
        self.audio_manager.play_coin_sound()
        self.player.add_coin()
        coin.kill()
        print(f"Handled coin collision at {(coin.rect.x, coin.rect.y)}")  # Logging handled collisions

    def check_collisions(self):
        # Check for collisions between the player and enemies/coins using a more efficient batch collision check method

        # Batch check for enemy collisions with the player using circle collision as a broad phase check
        for enemy in self.enemies:
            if pygame.sprite.collide_rect(self.player, enemy):
                if pygame.sprite.collide_mask(self.player, enemy):
                    self.handle_enemy_collision(enemy)

            # Checking if enemy is in warp field
            if self.player.warp_field_enabled and self.player.is_point_in_warp_field(enemy.rect.center):
                enemy.in_warp_field = True
            else:
                enemy.in_warp_field = False

        # Check for collisions between the player and coins using rect and mask collision checks
        for coin in self.coins:
            if pygame.sprite.collide_rect(self.player, coin):
                if pygame.sprite.collide_mask(self.player, coin):
                    self.handle_coin_collision(coin)
                    coin.kill()
