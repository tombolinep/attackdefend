import pygame
import sys
from model.game_model import GameModel
from controller.game_controller import GameController
from src.view.game_view import GameView


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Attack and Defend')
    clock = pygame.time.Clock()

    model = GameModel()
    view = GameView()
    controller = GameController(model, view, screen)

    while model.running:
        controller.handle_events()
        controller.update_game()

        screen.fill((0, 0, 0))
        model.all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
