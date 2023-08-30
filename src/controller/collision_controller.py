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

    def collision_circle_rectangle(self, circle_sprite, rectangle_sprite):
        dx = circle_sprite.rect.centerx - rectangle_sprite.rect.centerx
        dy = circle_sprite.rect.centery - rectangle_sprite.rect.centery

        closest_x = max(rectangle_sprite.rect.left, min(circle_sprite.rect.centerx, rectangle_sprite.rect.right))
        closest_y = max(rectangle_sprite.rect.top, min(circle_sprite.rect.centery, rectangle_sprite.rect.bottom))
        dist_x = circle_sprite.rect.centerx - closest_x
        dist_y = circle_sprite.rect.centery - closest_y

        return math.sqrt(dist_x ** 2 + dist_y ** 2) < circle_sprite.diameter / 2

    def handle_enemy_collision(self, enemy):
        if self.player.get_shield() > 0:
            self.audio_manager.play_shield_hit_sound()
            self.player.remove_shield()
            enemy.kill()
        else:
            self.audio_manager.play_death_sound()
            should_restart = GameView.display_game_over(self.screen)
            if should_restart:
                self.reset_game()
            else:
                self.running = False

    def handle_powerup_collision(self, powerup):
        self.audio_manager.play_powerup_sound()
        powerup.apply_powerup(self.enemies)
        powerup.kill()

    def handle_coin_collision(self, coin):
        self.audio_manager.play_coin_sound()
        self.player.add_coin()
        coin.kill()

    def check_collisions(self):
        colliding_enemy = pygame.sprite.spritecollideany(self.player, self.enemies,
                                                         collided=self.collision_circle_rectangle)
        if colliding_enemy:
            self.handle_enemy_collision(colliding_enemy)

        colliding_powerup = pygame.sprite.spritecollideany(self.player, self.powerups)
        if colliding_powerup:
            self.handle_powerup_collision(colliding_powerup)

        colliding_coin = pygame.sprite.spritecollideany(self.player, self.coins)
        if colliding_coin:
            self.handle_coin_collision(colliding_coin)

        colliding_bullet_enemy = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        for enemy_list in colliding_bullet_enemy.values():
            for enemy in enemy_list:
                enemy.kill()
