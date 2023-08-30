import random
from math import sqrt

import pygame
from src.constants import POWERUP_INTERVAL, SCREEN_HEIGHT, BULLET_INTERVAL, \
    SCREEN_WIDTH, STATS_WIDTH, COIN_SIZE, POWERUP_SIZE  # Replace with your actual constants file
from src.model.audio_manager import Audio
from src.model.bullet import Bullet
from src.model.coin import Coin
from src.model.enemy import Enemy
from src.model.powerup import PowerUp


class GameModel:
    def __init__(self):
        self.audio_manager = Audio()
        self.running = True
        self.paused = False
        self.score = 0
        self.player = None
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.next_powerup_time = pygame.time.get_ticks() + POWERUP_INTERVAL
        self.next_bullet_time = pygame.time.get_ticks()

    def stop_game(self):
        self.running = False

    def set_player(self, player):
        self.player = player
        self.all_sprites.add(player)

    def add_enemy(self):
        enemy_type = "red" if random.random() < 0.1 else "white"
        enemy = Enemy(self.score, enemy_type)
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)

    def add_powerup(self):
        x = random.randint(STATS_WIDTH, SCREEN_WIDTH - POWERUP_SIZE)
        y = random.randint(0, SCREEN_HEIGHT - POWERUP_SIZE)
        powerup = PowerUp(x, y)
        self.powerups.add(powerup)
        self.all_sprites.add(powerup)

    def add_coin(self):
        x = random.randint(STATS_WIDTH, SCREEN_WIDTH - COIN_SIZE)
        y = random.randint(0, SCREEN_HEIGHT - COIN_SIZE)
        coin = Coin(x, y)
        self.coins.add(coin)
        self.all_sprites.add(coin)

    def find_closest_enemy(self):
        closest_enemy = None
        closest_distance = float("inf")

        for enemy in self.enemies:
            dx = enemy.rect.x - self.player.rect.x
            dy = enemy.rect.y - self.player.rect.y
            distance = sqrt(dx ** 2 + dy ** 2)

            if distance < closest_distance:
                closest_distance = distance
                closest_enemy = enemy

        return closest_enemy

    def calculate_target(self, closest_enemy):
        dx = closest_enemy.rect.x - self.player.rect.x
        dy = closest_enemy.rect.y - self.player.rect.y
        scale = SCREEN_HEIGHT / abs(dy)

        target_x = self.player.rect.x + dx * scale
        target_y = self.player.rect.y + dy * scale

        return target_x, target_y

    def automatic_shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time >= self.next_bullet_time:
            closest_enemy = self.find_closest_enemy()

            if closest_enemy:
                target_x, target_y = self.calculate_target(closest_enemy)
                bullet = Bullet(self.player.rect.x, self.player.rect.y, target_x, target_y)
                self.add_bullet(bullet)

            # Reset the timer
            self.next_bullet_time = current_time + BULLET_INTERVAL

    def add_bullet(self, bullet):
        self.bullets.add(bullet)
        self.all_sprites.add(bullet)

    def increment_score(self):
        self.score += 1
