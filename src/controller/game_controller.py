import pygame

from src.controller.collision_controller import CollisionController
from src.controller.enemy_controller import EnemyController
from src.controller.player_controller import PlayerController
from src.model.player import Player
from src.view.player_view import PlayerView


class GameController:
    def __init__(self, model, view, screen):
        self.model = model
        self.view = view
        self.initialize_game()
        self.enemy_controller = EnemyController(model.enemies)
        self.collision_controller = CollisionController(model, screen)

    def initialize_game(self):
        # Initialize player and player view
        player = Player()
        player_view = PlayerView(player)

        # Set player model and view in main model and view
        self.model.set_player(player)
        self.view.set_player_view(player_view)

        # Initialize player controller with the player model and view
        self.player_controller = PlayerController(player, player_view)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.model.stop_game()
            # Add other event handling logic here

    def update_game(self):
        pressed_keys = pygame.key.get_pressed()
        self.player_controller.update(pressed_keys)  # Removed the duplicate line
        self.model.increment_score()  # Should be a method in GameModel
        self.enemy_controller.update()
        self.collision_controller.check_collisions()
