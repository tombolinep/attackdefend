import pygame

from src.controller.collision_controller import CollisionController
from src.controller.enemy_controller import EnemyController
from src.controller.player_controller import PlayerController
from src.model.player import Player
from src.view.player_view import PlayerView


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
            elif event.type == self.time_manager.ADDENEMY:
                self.model.add_enemy()
            elif event.type == self.time_manager.ADDCOIN:
                self.model.add_coin()
            elif event.type == self.time_manager.ADDPOWERUP:
                self.model.add_powerup()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.event_dispatcher.handle_event(event)
            elif event.type == self.time_manager.SHOOT:
                self.model.automatic_shoot()

    def update_game(self):
        pressed_keys = pygame.key.get_pressed()
        self.player_controller.update(pressed_keys)
        self.model.increment_score()
        self.enemy_controller.update()
        self.collision_controller.check_collisions()
        self.model.automatic_shoot()
        self.model.bullets.update()
        self.model.coins.update()

    def update_and_render(self):
        self.handle_events()
        if not self.model.paused:
            self.update_game()
        self.view.render(self.model)
