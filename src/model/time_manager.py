import pygame

from src.constants import POWERUP_INTERVAL, COIN_INTERVAL


class TimeManager:
    def __init__(self):
        self.initialize_events()
        self.time_since_last_enemy = 0
        self.time_since_last_powerup = 0
        self.time_since_last_coin = 0

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
        # Capture the current time remaining for each event
        self.time_since_last_enemy = pygame.time.get_ticks() % 250
        self.time_since_last_powerup = pygame.time.get_ticks() % POWERUP_INTERVAL
        self.time_since_last_coin = pygame.time.get_ticks() % COIN_INTERVAL
        pygame.time.set_timer(self.ADDENEMY, 0)
        pygame.time.set_timer(self.ADDPOWERUP, 0)
        pygame.time.set_timer(self.ADDCOIN, 0)

    def resume_timers(self):
        # Set the timers to the remaining time
        pygame.time.set_timer(self.ADDENEMY, 250 - self.time_since_last_enemy)
        pygame.time.set_timer(self.ADDPOWERUP, POWERUP_INTERVAL - self.time_since_last_powerup)
        pygame.time.set_timer(self.ADDCOIN, COIN_INTERVAL - self.time_since_last_coin)

        # Subsequent events will be back to the original interval
        pygame.time.set_timer(self.ADDENEMY, 250, True)
        pygame.time.set_timer(self.ADDPOWERUP, POWERUP_INTERVAL, True)
        pygame.time.set_timer(self.ADDCOIN, COIN_INTERVAL, True)
