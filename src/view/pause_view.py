import pygame

# Constants
SCREEN_WIDTH = 1536
SCREEN_HEIGHT = 864
STATS_WIDTH = 350
MAIN_GAME_WIDTH = SCREEN_WIDTH - STATS_WIDTH


class PauseView:
    def __init__(self, model, controller):
        self.model = model
        self.controller = controller

    def draw(self, screen):
        # Create a surface that will act as a semi-transparent overlay for the main game area (excluding stats screen)
        s = pygame.Surface((MAIN_GAME_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))  # (R, G, B, Alpha)

        # Calculate the position for the parallel rectangles (Pause symbol)
        rect1_x = STATS_WIDTH + (MAIN_GAME_WIDTH // 2) - 20  # A bit to the left from the center
        rect2_x = STATS_WIDTH + (MAIN_GAME_WIDTH // 2) + 10  # A bit to the right from the center
        rect_y = SCREEN_HEIGHT // 2 - 30  # Vertically centered, made them shorter
        rect_width = 20  # Made them wider
        rect_height = 60  # Made them shorter

        # Draw two parallel rectangles on the surface
        rect_color = (255, 255, 255)  # White color
        pygame.draw.rect(s, rect_color, (rect1_x - STATS_WIDTH, rect_y, rect_width, rect_height))  # Rect1
        pygame.draw.rect(s, rect_color, (rect2_x - STATS_WIDTH, rect_y, rect_width, rect_height))  # Rect2

        # Draw the surface on the main game screen
        screen.blit(s, (STATS_WIDTH, 0))
