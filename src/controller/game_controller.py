import logging

import pygame
from pygame import KEYDOWN, K_r, K_q, K_ESCAPE, QUIT

from src.controller.collision_controller import CollisionController
from src.controller.enemy_controller import EnemyController
from src.controller.player_controller import PlayerController
from src.controller.shop_controller import ShopController
from src.model.pause import PauseModel
from src.model.player import Player
from src.model.shop import Shop
from src.view.pause_view import PauseView
from src.view.player_view import PlayerView
from src.view.shop_view import ShopView

logging.basicConfig(level=logging.DEBUG)


class GameController:
    def __init__(self, model, view, screen, event_dispatcher, time_manager):
        self.model = model
        self.view = view
        self.screen = screen
        self.event_dispatcher = event_dispatcher
        self.time_manager = time_manager
        self.initialize_game()
        self.enemy_controller = EnemyController(model.enemies)
        self.collision_controller = CollisionController(model, screen)
        self.event_dispatcher.view = view
        self.event_dispatcher.add_listener("pause_game", self.toggle_pause)
        self.event_dispatcher.add_listener("open_shop", self.open_shop)
        self.pause_model = PauseModel()
        self.pause_view = PauseView(self.pause_model, self)
        self.last_log_time = 0
        self.coin_start_time = None
        self.powerup_start_time = None
        self.coin_interval = time_manager.COIN_INTERVAL
        self.powerup_interval = time_manager.POWERUP_INTERVAL

    def initialize_game(self):
        player = Player()
        player_view = PlayerView(player)

        self.model.set_player(player)
        self.view.set_player_view(player_view)

        self.player_controller = PlayerController(player, player_view)
        self.model.audio_manager.play_bg_music()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.model.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.model.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                self.check_buttons(mouse_pos)
            elif not self.model.paused:
                if event.type == self.time_manager.ADDENEMY:
                    self.model.add_enemy()
                elif event.type == self.time_manager.ADDCOIN:
                    self.coin_start_time = pygame.time.get_ticks()
                    self.model.add_coin()
                elif event.type == self.time_manager.ADDPOWERUP:
                    self.powerup_start_time = pygame.time.get_ticks()
                    self.model.add_powerup()
                elif event.type == self.time_manager.SHOOT:
                    self.model.automatic_shoot()

    def update_game(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_log_time >= 1000:
            self.last_log_time = current_time
            self.update_timer_logs()
        if not self.model.paused:
            pressed_keys = pygame.key.get_pressed()
            self.player_controller.update(pressed_keys)
            self.model.increment_score()
            self.enemy_controller.update()
            self.collision_controller.check_collisions()
            self.model.automatic_shoot()
            self.model.bullets.update()
            self.model.coins.update()
            self.model.powerups.update()

    def update_timer_logs(self):
        current_time = pygame.time.get_ticks()
        if self.coin_start_time:
            coin_time_remaining = self.coin_interval - (current_time - self.coin_start_time)
            # logging.info(f"Coin Timer: {coin_time_remaining}ms remaining")
        if self.powerup_start_time:
            powerup_time_remaining = self.powerup_interval - (current_time - self.powerup_start_time)
            # logging.info(f"Powerup Timer: {powerup_time_remaining}ms remaining")

    def update_and_render(self):
        self.update_game()  # Always update the game state
        self.render()  # Always render the main view and overlay pause view if needed

    def render(self):
        if not self.model.paused:
            self.view.render(self.model)  # Continue to render the main game view
            pygame.display.update()  # Update the screen regardless of game state

    def handle_game_over(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Retry
                    self.model.reset_game()
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:  # Quit
                    self.model.running = False
            elif event.type == pygame.QUIT:
                self.model.running = False

    def toggle_pause(self, data=None):
        self.model.paused = not self.model.paused
        if self.model.paused:
            self.pause_view.draw(self.screen)
        pygame.display.flip()

    def check_buttons(self, mouse_pos):
        for button in self.view.buttons:
            if button.rect.collidepoint(mouse_pos):
                if button.text == "Pause" or button.text == "Resume":
                    self.event_dispatcher.dispatch_event("pause_game", {})  # Ensuring the pause event is dispatched
                elif button.text == "Shop":
                    self.event_dispatcher.dispatch_event("open_shop", {})

    def open_shop(self, data=None):
        shop_model = Shop(self.model.player)
        shop_view = ShopView(shop_model, self, self.event_dispatcher)  # pass in 'self' as GameController object
        shop_controller = ShopController(shop_model, shop_view, self.screen, self.event_dispatcher)
        powerup_type = shop_controller.open_shop(self.model.player)
