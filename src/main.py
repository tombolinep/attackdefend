import cProfile
import sys
import pygame
from model.GameSettings import GameSettings
from model.game_model import GameModel
from controller.game_controller import GameController
from events.events import EventDispatcher
from model.time_manager import TimeManager
from view.game_view import GameView
from view.pause_view import PauseView
from view.gameover_view import GameOverView
from constants import MIN_SCREEN_WIDTH, MIN_SCREEN_HEIGHT, MAX_SCREEN_WIDTH, \
    MAX_SCREEN_HEIGHT


def main():
    pygame.init()
    game_settings = GameSettings()

    flags = pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE
    screen = pygame.display.set_mode((game_settings.SCREEN_WIDTH, game_settings.SCREEN_HEIGHT), flags)
    pygame.display.set_caption('SpaceJungle')

    clock = pygame.time.Clock()

    model = GameModel(game_settings)
    view = GameView(screen, game_settings)
    pause_view = PauseView(game_settings)
    game_over_view = GameOverView(game_settings)
    event_dispatcher = EventDispatcher()
    time_manager = TimeManager()
    controller = GameController(model, view, screen, event_dispatcher, time_manager, game_settings)

    while model.running:
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                new_size = event.size
                new_width = max(MIN_SCREEN_WIDTH, min(new_size[0], MAX_SCREEN_WIDTH))
                new_height = max(MIN_SCREEN_HEIGHT, min(new_size[1], MAX_SCREEN_HEIGHT))

                # Maintain the aspect ratio based on the default width and height
                aspect_ratio = game_settings.SCREEN_WIDTH / game_settings.SCREEN_HEIGHT
                new_height = int(new_width / aspect_ratio)

                game_settings.update_screen_dimensions(new_width, new_height)
                screen = pygame.display.set_mode((new_width, new_height), flags)
                view.update_dimensions()

            controller.handle_events()  # Forward events to existing event handlers

        if model.game_over:
            controller.handle_game_over()
            game_over_view.draw(screen, model)
            pygame.display.flip()
        else:
            if model.paused:
                pause_view.draw(screen)
                pygame.display.flip()
            else:
                controller.update_and_render()
                clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    cProfile.run('main()', 'profile_result.out')
