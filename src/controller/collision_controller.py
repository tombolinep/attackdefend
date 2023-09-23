import math
import random

import pygame
import pygame.gfxdraw

from constants import ENEMY_COIN_CHANCE


def apply_powerup(enemies_group):
    white_enemies = [enemy for enemy in enemies_group if enemy.type == "white"]
    for enemy in white_enemies:
        enemy.kill()


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
                self.model.spawn_coin_at_location(enemy.rect.center[0], enemy.rect.center[1])
            enemy.kill()
            self.model.score += 50
        else:
            self.audio_manager.play_death_sound()
            self.model.set_game_over(True)

    def handle_coin_collision(self, coin):
        self.audio_manager.play_coin_sound()
        self.player.add_coin()
        coin.kill()

    def handle_powerup_collision(self, powerup):
        self.audio_manager.play_powerup_sound()
        apply_powerup(self.enemies)
        powerup.kill()
        self.model.score += 300

    def handle_laser_collision(self, enemy):
        if random.random() < ENEMY_COIN_CHANCE:
            self.model.spawn_coin_at_location(enemy.rect.center[0], enemy.rect.center[1])
        enemy.kill()
        self.model.score += 50

    def handle_bullet_collision(self, enemy):
        if random.random() < ENEMY_COIN_CHANCE:
            self.model.spawn_coin_at_location(enemy.rect.center[0], enemy.rect.center[1])
        enemy.kill()
        self.model.score += 50

    def calculate_distance(self, point1, point2):
        dx = point1[0] - point2[0]
        dy = point1[1] - point2[1]
        return math.sqrt(dx * dx + dy * dy)

    def is_in_explosion_radius(self, rocket, enemy):
        distance = self.calculate_distance(
            (rocket.rect.centerx, rocket.rect.centery),
            (enemy.rect.centerx, enemy.rect.centery)
        )
        return distance <= rocket.explosion_radius

    def handle_rocket_collision(self, rocket, enemy):
        if rocket.is_exploding:
            if self.is_in_explosion_radius(rocket, enemy):
                if random.random() < ENEMY_COIN_CHANCE:
                    self.model.spawn_coin_at_location(enemy.rect.x, enemy.rect.y)
                enemy.kill()
                self.model.score += 50

    def check_collisions(self):
        for enemy in self.enemies:
            if pygame.sprite.collide_rect(self.player, enemy):
                if pygame.sprite.collide_mask(self.player, enemy):
                    self.handle_enemy_collision(enemy)
            # if self.player.warp_field_enabled and self.player.is_point_in_warp_field(enemy.rect.center):
            #     enemy.in_warp_field = True
            # else:
            #     enemy.in_warp_field = False

        for coin in self.coins:
            if pygame.sprite.collide_rect(self.player, coin):
                if pygame.sprite.collide_mask(self.player, coin):
                    self.handle_coin_collision(coin)
                    coin.kill()

        for powerup in self.powerups:
            if pygame.sprite.collide_rect(self.player, powerup):
                if pygame.sprite.collide_mask(self.player, powerup):
                    self.handle_powerup_collision(powerup)
                    powerup.kill()

        for laser in self.lasers:
            collided_enemy = pygame.sprite.spritecollideany(laser, self.enemies)
            if collided_enemy:
                self.handle_laser_collision(collided_enemy)

        for rocket in self.rockets:
            collided_enemy = pygame.sprite.spritecollideany(rocket, self.enemies)
            if collided_enemy:
                self.handle_rocket_collision(rocket, collided_enemy)

        colliding_bullet_enemy = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        for enemy_list in colliding_bullet_enemy.values():
            for enemy in enemy_list:
                self.handle_bullet_collision(enemy)
