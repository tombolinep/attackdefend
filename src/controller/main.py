import pygame

from src.controller.game import Game


def main():
    try:
        pygame.init()
        game_instance = Game()
        game_instance.run()
        game_instance.quit_game()
    except Exception as e:
        print("An error occurred:", e)
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
