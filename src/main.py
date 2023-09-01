import pygame
import sys
from model.game_model import GameModel
from controller.game_controller import GameController
from src.events.events import EventDispatcher
from src.model.time_manager import TimeManager
from src.view.game_view import GameView
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('SpaceJungle')
    clock = pygame.time.Clock()

    model = GameModel()
    view = GameView(screen)
    event_dispatcher = EventDispatcher()
    time_manager = TimeManager()
    controller = GameController(model, view, screen, event_dispatcher, time_manager)

    while model.running:
        controller.handle_events()
        controller.update_and_render()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
