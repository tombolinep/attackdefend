import pygame

from src.model.enemy import Enemy
from src.model.coin import Coin
from src.model.powerup import PowerUp
import random
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH, POWERUP_INTERVAL


class GameManager:
    def __init__(self):
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.score = 0
        self.next_powerup_time = pygame.time.get_ticks() + POWERUP_INTERVAL

    def add_entity(self):
        if random.random() < 0.1:
            enemy_type = "red"
        else:
            enemy_type = "white"
        new_enemy = Enemy(self.score, enemy_type)
        self.enemies.add(new_enemy)
        self.all_sprites.add(new_enemy)

    def add_coin(self):
        coin_x = random.randint(STATS_WIDTH, SCREEN_WIDTH - 20)
        coin_y = random.randint(0, SCREEN_HEIGHT - 20)
        new_coin = Coin(coin_x, coin_y)
        self.coins.add(new_coin)
        self.all_sprites.add(new_coin)

    def add_powerup(self):
        new_powerup = PowerUp()
        self.powerups.add(new_powerup)
        self.all_sprites.add(new_powerup)
        self.next_powerup_time = pygame.time.get_ticks() + POWERUP_INTERVAL
