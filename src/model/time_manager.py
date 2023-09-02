import pygame
from src.constants import POWERUP_INTERVAL, COIN_INTERVAL
import logging


class TimeManager:
    def __init__(self):
        self.COIN_INTERVAL = COIN_INTERVAL  # Assuming COIN_INTERVAL is defined elsewhere
        self.POWERUP_INTERVAL = POWERUP_INTERVAL  # Assuming POWERUP_INTERVAL is defined elsewhere

        self.coin_timer_active = True
        self.powerup_timer_active = True
        self.initialize_events()

    def initialize_events(self):
        self.ADDENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADDENEMY, 250)

        self.SHOOT = pygame.USEREVENT + 2
        pygame.time.set_timer(self.SHOOT, 4200)

        self.ADDCOIN = pygame.USEREVENT + 3
        pygame.time.set_timer(self.ADDCOIN, self.COIN_INTERVAL)
        logging.info(f"Coin Timer Initialized: {self.COIN_INTERVAL}")

        self.ADDPOWERUP = pygame.USEREVENT + 4
        pygame.time.set_timer(self.ADDPOWERUP, self.POWERUP_INTERVAL)
        logging.info(f"Powerup Timer Initialized: {self.POWERUP_INTERVAL}")

    def pause_timers(self):
        self.coin_timer_active = pygame.time.get_timer(self.ADDCOIN) != 0
        self.powerup_timer_active = pygame.time.get_timer(self.ADDPOWERUP) != 0

        pygame.time.set_timer(self.ADDCOIN, 0)
        pygame.time.set_timer(self.ADDPOWERUP, 0)

    def resume_timers(self):
        current_time = pygame.time.get_ticks()

        pygame.time.set_timer(self.ADDENEMY, 250 - self.time_since_last_enemy + current_time % 250)
        pygame.time.set_timer(self.ADDPOWERUP,
                              POWERUP_INTERVAL - self.time_since_last_powerup + current_time % POWERUP_INTERVAL)
        pygame.time.set_timer(self.ADDCOIN, COIN_INTERVAL - self.time_since_last_coin + current_time % COIN_INTERVAL)

    def update_last_coin_time(self):
        self.last_coin_time = pygame.time.get_ticks()

    def update_last_powerup_time(self):
        self.last_powerup_time = pygame.time.get_ticks()
