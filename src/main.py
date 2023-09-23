import cProfile
import sys
import pygame
from model.game_settings import GameSettings
from model.game_model import GameModel
from controller.game_controller import GameController
from events.events import EventDispatcher
from model.time_manager import TimeManager
from view.game_view import GameView
from view.pause_view import PauseView
from view.gameover_view import GameOverView


def main():
    pygame.init()
    game_settings = GameSettings()
    screen = pygame.display.set_mode((game_settings.SCREEN_WIDTH, game_settings.SCREEN_HEIGHT), game_settings.flags)
    pygame.display.set_caption('SpaceJungle')
    clock = pygame.time.Clock()

    model = GameModel(game_settings)
    view = GameView(screen, game_settings)
    pause_view = PauseView()
    game_over_view = GameOverView(game_settings)
    event_dispatcher = EventDispatcher()
    time_manager = TimeManager()
    controller = GameController(model, view, screen, event_dispatcher, time_manager, game_settings)

    while model.running:
        if model.game_over:
            controller.handle_game_over()
            game_over_view.draw(screen, model)
            pygame.display.flip()
        else:
            controller.handle_events()

            if model.paused:
                pause_view.draw(screen, game_settings)
                pygame.display.flip()
            else:
                controller.update_and_render()
                clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    cProfile.run('main()', 'profile_result.out')
