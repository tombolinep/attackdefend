import pygame
from constants import POWERUP_INTERVAL, COIN_INTERVAL, BULLET_INTERVAL, ROCKET_INTERVAL, LASER_INTERVAL, ENEMY_INTERVAL


class TimeManager:
    def __init__(self):
        self.coin_timer_active = True
        self.powerup_timer_active = True
        self.initialize_events()

    def initialize_events(self):
        self.ADDENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADDENEMY, ENEMY_INTERVAL)

        self.SHOOT = pygame.USEREVENT + 2
        pygame.time.set_timer(self.SHOOT, BULLET_INTERVAL)

        self.ADDCOIN = pygame.USEREVENT + 3
        pygame.time.set_timer(self.ADDCOIN, COIN_INTERVAL)

        self.ADDPOWERUP = pygame.USEREVENT + 4
        pygame.time.set_timer(self.ADDPOWERUP, POWERUP_INTERVAL)

        self.ROCKET_SHOOT = pygame.USEREVENT + 5
        pygame.time.set_timer(self.ROCKET_SHOOT, ROCKET_INTERVAL)

        self.LASER_SHOOT = pygame.USEREVENT + 6
        pygame.time.set_timer(self.LASER_SHOOT, LASER_INTERVAL)
