import logging

import pygame
from pygame import KEYDOWN, K_r, K_q, K_ESCAPE, QUIT

from constants import COIN_INTERVAL, POWERUP_INTERVAL, MIN_SCREEN_WIDTH, MAX_SCREEN_WIDTH, MAX_SCREEN_HEIGHT, \
    MIN_SCREEN_HEIGHT
from controller.collision_controller import CollisionController
from controller.enemy_controller import EnemyController
from controller.player_controller import PlayerController
from controller.shop_controller import ShopController
from model.pause import PauseModel
from model.player import Player
from model.shop import Shop
from view.player_view import PlayerView
from view.shop_view import ShopView

logging.basicConfig(level=logging.DEBUG)


class GameController:
    def __init__(self, model, view, screen, event_dispatcher, time_manager, settings):
        self.settings = settings
        self.player_controller = None
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
        self.last_log_time = 0
        self.coin_start_time = None
        self.powerup_start_time = None
        self.coin_interval = COIN_INTERVAL
        self.powerup_interval = POWERUP_INTERVAL
        self.shop_model = Shop(self.model.player, model.audio_manager)
        self.shop_view = ShopView(self.shop_model, self, self.event_dispatcher, self.settings)
        self.shop_controller = ShopController(self.shop_model, self.shop_view, self.screen, self.event_dispatcher)
        self.music_muted = False

    def initialize_game(self):
        player = self.model.player
        player_view = PlayerView(player)
        self.view.set_player_view(player_view)
        self.player_controller = PlayerController(player, player_view, self.settings)

        # self.model.audio_manager.play_bg_music()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.model.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.model.running = False
                if event.key == pygame.K_p:
                    self.model.paused = not self.model.paused
                elif event.key == pygame.K_m:
                    if not self.music_muted:
                        self.music_muted = True
                        self.model.audio_manager.stop_bg_music()
                    else:
                        self.model.audio_manager.play_bg_music()
                        self.music_muted = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                self.check_buttons(mouse_pos)
            elif event.type == pygame.VIDEORESIZE:
                self.handle_resize_event(event)
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
                elif event.type == self.time_manager.ROCKET_SHOOT:
                    self.model.rocket_shoot()
                elif event.type == self.time_manager.LASER_SHOOT:
                    self.model.laser_shoot()

    def update_game(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_log_time >= 1000:
            self.last_log_time = current_time
        if not self.model.paused:
            pressed_keys = pygame.key.get_pressed()
            self.player_controller.update(pressed_keys)
            self.model.increment_score()
            self.enemy_controller.update()
            self.collision_controller.check_collisions()
            self.model.automatic_shoot()
            self.model.bullets.update()
            self.model.rockets.update()
            self.model.lasers.update()
            self.model.coins.update()
            self.model.powerups.update()
            self.model.tractor_beams.update()
            self.model.warp_fields.update()
            self.model.shields.update()

    def update_and_render(self):
        if not self.model.paused:
            self.update_game()
            self.view.render(self.model)

    def handle_game_over(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.model.reset_game()
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    self.model.running = False
            elif event.type == pygame.QUIT:
                self.model.running = False

    def toggle_pause(self, data=None):
        self.model.paused = not self.model.paused

    def check_buttons(self, mouse_pos):
        for button in self.view.buttons:
            if button.rect.collidepoint(mouse_pos):
                if button.text == "Pause" or button.text == "Resume":
                    self.event_dispatcher.dispatch_event("pause_game", {})
                elif button.text == "Shop":
                    self.event_dispatcher.dispatch_event("open_shop", {})

    def open_shop(self, data=None):
        powerup_type = self.shop_controller.open_shop(self.model.player)

    def handle_resize_event(self, event):
        new_size = event.size
        new_width = max(MIN_SCREEN_WIDTH, min(new_size[0], MAX_SCREEN_WIDTH))
        new_height = max(MIN_SCREEN_HEIGHT, min(new_size[1], MAX_SCREEN_HEIGHT))

        aspect_ratio = self.settings.SCREEN_WIDTH / self.settings.SCREEN_HEIGHT
        calculated_height = int(new_width / aspect_ratio)
        new_height = max(MIN_SCREEN_HEIGHT, min(calculated_height, MAX_SCREEN_HEIGHT))

        if new_height != calculated_height:
            new_width = int(new_height * aspect_ratio)

        self.settings.update_screen_dimensions(new_width, new_height)
        self.screen = pygame.display.set_mode((new_width, new_height), self.settings.flags)

        self.view.update_button_positions()
        self.view.resize_background(new_width, new_height)
        self.shop_view.update_view(self.settings)
