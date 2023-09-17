import pygame
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH, MAIN_GAME_WIDTH


class PauseView:
    def draw(self, screen):
        # Create a surface with an alpha channel (transparency)
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        # Define the pause symbol (two parallel rectangles)
        pause_color = (255, 255, 255)  # White color
        rect_width = 20
        rect_height = 60
        rect1_x = STATS_WIDTH + MAIN_GAME_WIDTH // 2 - 30  # Centered considering the STATS_WIDTH
        rect2_x = STATS_WIDTH + MAIN_GAME_WIDTH // 2 + 10  # Centered considering the STATS_WIDTH
        rect_y = SCREEN_HEIGHT // 2 - 30

        # Draw the pause symbol on the surface
        pygame.draw.rect(s, pause_color, (rect1_x, rect_y, rect_width, rect_height))
        pygame.draw.rect(s, pause_color, (rect2_x, rect_y, rect_width, rect_height))

        # Blit the surface onto the screen
        screen.blit(s, (0, 0))
