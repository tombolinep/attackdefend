import pygame
import sys
import cProfile  # Import cProfile module
from model.game_model import GameModel
from controller.game_controller import GameController
from events.events import EventDispatcher
from model.time_manager import TimeManager
from view.game_view import GameView
from view.pause_view import PauseView
from view.gameover_view import GameOverView
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), vsync=1)
    pygame.display.set_caption('SpaceJungle')
    clock = pygame.time.Clock()

    model = GameModel()
    view = GameView(screen)
    pause_view = PauseView()
    game_over_view = GameOverView()
    event_dispatcher = EventDispatcher()
    time_manager = TimeManager()
    controller = GameController(model, view, screen, event_dispatcher, time_manager)

    while model.running:
        if model.game_over:
            controller.handle_game_over()
            game_over_view.draw(screen, model)
            pygame.display.flip()
        else:
            controller.handle_events()

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
