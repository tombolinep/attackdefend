import pygame
from src.constants import POWERUP_INTERVAL  # Replace with your actual constants file
from src.model.audio_manager import Audio


class GameModel:
    def __init__(self):
        self.audio_manager = Audio()
        self.running = True
        self.paused = False
        self.score = 0
        self.player = None  # To be initialized by GameController
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.next_powerup_time = pygame.time.get_ticks() + POWERUP_INTERVAL

    def stop_game(self):
        self.running = False

    def set_player(self, player):
        self.player = player
        self.all_sprites.add(player)

    def add_enemy(self, enemy):
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)

    def add_powerup(self, powerup):
        self.powerups.add(powerup)
        self.all_sprites.add(powerup)

    def add_coin(self, coin):
        self.coins.add(coin)
        self.all_sprites.add(coin)

    def add_bullet(self, bullet):
        self.bullets.add(bullet)
        self.all_sprites.add(bullet)

    def increment_score(self):
        self.score += 1
