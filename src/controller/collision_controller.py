import math

import pygame

from src.view.game_view import GameView


class CollisionController:
    def __init__(self, model, screen):
        self.model = model
        self.player = model.player
        self.enemies = model.enemies
        self.powerups = model.powerups
        self.coins = model.coins
        self.bullets = model.bullets
        self.audio_manager = model.audio_manager
        self.screen = screen
        self.running = model.running

    def collision_circle_rectangle(self, circle, rect):
        circle_distance_x = abs(circle.x - rect.x - rect.width // 2)
        circle_distance_y = abs(circle.y - rect.y - rect.height // 2)

        # If the circle and rectangle are far enough apart to not overlap, return False
        if circle_distance_x > (rect.width // 2 + circle.diameter // 2):
            return False
        if circle_distance_y > (rect.height // 2 + circle.diameter // 2):
            return False

        # If the circle's center is inside the rectangle, then they are colliding
        if circle_distance_x <= (rect.width // 2):
            return True
        if circle_distance_y <= (rect.height // 2):
            return True

        # Check for collision at rectangle corner.
        corner_distance_sq = (circle_distance_x - rect.width // 2) ** 2 + (circle_distance_y - rect.height // 2) ** 2

        return corner_distance_sq <= (circle.diameter // 2) ** 2

    def handle_enemy_collision(self, enemy):
        if self.player.get_shield() > 0:
            self.audio_manager.play_shield_hit_sound()
            self.player.remove_shield()
            enemy.kill()
        else:
            self.audio_manager.play_death_sound()
            self.model.set_game_over(True)

    def handle_powerup_collision(self, powerup):
        self.audio_manager.play_powerup_sound()
        powerup.apply_powerup(self.enemies)
        powerup.kill()

    def handle_coin_collision(self, coin):
        self.audio_manager.play_coin_sound()
        self.player.add_coin()
        coin.kill()

    def check_collisions(self):
        for enemy in self.enemies:
            if self.collision_circle_rectangle(self.player, enemy.rect):
                self.handle_enemy_collision(enemy)

        for powerup in self.powerups:
            if self.collision_circle_rectangle(self.player, powerup.rect):
                self.handle_powerup_collision(powerup)

        for coin in self.coins:
            if self.collision_circle_rectangle(self.player, coin.rect):
                self.handle_coin_collision(coin)

        colliding_bullet_enemy = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        for enemy_list in colliding_bullet_enemy.values():
            for enemy in enemy_list:
                enemy.kill()
