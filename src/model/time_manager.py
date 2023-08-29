import pygame

from src.constants import POWERUP_INTERVAL, COIN_INTERVAL


class TimeManager:
    def __init__(self):
        self.initialize_events()

    def initialize_events(self):
        self.ADDENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADDENEMY, 250)

        self.ADDPOWERUP = pygame.USEREVENT + 2
        pygame.time.set_timer(self.ADDPOWERUP, POWERUP_INTERVAL)

        self.ADDCOIN = pygame.USEREVENT + 3
        pygame.time.set_timer(self.ADDCOIN, COIN_INTERVAL)

        self.SHOOT = pygame.USEREVENT + 4
        pygame.time.set_timer(self.SHOOT, 4200)

    def pause_timers(self):
        pygame.time.set_timer(self.ADDENEMY, 0)
        pygame.time.set_timer(self.ADDPOWERUP, 0)
        pygame.time.set_timer(self.ADDCOIN, 0)

    def resume_timers(self):
        pygame.time.set_timer(self.ADDENEMY, 250)
        pygame.time.set_timer(self.ADDPOWERUP, POWERUP_INTERVAL)
        pygame.time.set_timer(self.ADDCOIN, COIN_INTERVAL)
