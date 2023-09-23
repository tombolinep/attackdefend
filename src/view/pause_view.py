import pygame


class PauseView:
    def draw(self, screen, settings):
        self.settings = settings
        # Create a surface with an alpha channel (transparency)
        s = pygame.Surface((self.settings.SCREEN_WIDTH, self.settings.SCREEN_HEIGHT), pygame.SRCALPHA)

        # Define the pause symbol (two parallel rectangles)
        pause_color = (255, 255, 255)  # White color
        rect_width = 20
        rect_height = 60
        rect1_x = self.settings.STATS_WIDTH + self.settings.MAIN_GAME_WIDTH // 2 - 30  # Centered considering the STATS_WIDTH
        rect2_x = self.settings.STATS_WIDTH + self.settings.MAIN_GAME_WIDTH // 2 + 10  # Centered considering the STATS_WIDTH
        rect_y = self.settings.SCREEN_HEIGHT // 2 - 30

        # Draw the pause symbol on the surface
        pygame.draw.rect(s, pause_color, (rect1_x, rect_y, rect_width, rect_height))
        pygame.draw.rect(s, pause_color, (rect2_x, rect_y, rect_width, rect_height))

        # Blit the surface onto the screen
        screen.blit(s, (0, 0))
