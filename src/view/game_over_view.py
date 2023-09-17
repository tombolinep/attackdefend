import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH, MAIN_GAME_WIDTH


class GameOverView:
    def __init__(self):
        self.font = pygame.font.Font(None, 74)
        self.score_font = pygame.font.Font(None, 50)
        self.instruction_font = pygame.font.Font(None, 36)

    def draw(self, screen, model):
        # Create text surfaces with a shadow effect
        text_surface = self.font.render('Game Over', True, (255, 0, 0))
        text_shadow_surface = self.font.render('Game Over', True, (128, 0, 0))

        score_text = f'Score: {model.score}'
        score_surface = self.score_font.render(score_text, True, (255, 255, 255))
        score_shadow_surface = self.score_font.render(score_text, True, (128, 128, 128))

        instruction_surface = self.instruction_font.render('Press R to Retry or Q to Quit', True, (255, 255, 255))
        instruction_shadow_surface = self.instruction_font.render('Press R to Retry or Q to Quit', True,
                                                                  (128, 128, 128))

        # Get rect objects for text and shadow surfaces
        text_rect = text_surface.get_rect(center=(STATS_WIDTH + MAIN_GAME_WIDTH / 2, SCREEN_HEIGHT / 2 - 100))
        text_shadow_rect = text_shadow_surface.get_rect(center=(text_rect.centerx + 3, text_rect.centery + 3))

        score_rect = score_surface.get_rect(center=(STATS_WIDTH + MAIN_GAME_WIDTH / 2, SCREEN_HEIGHT / 2 - 20))
        score_shadow_rect = score_shadow_surface.get_rect(center=(score_rect.centerx + 2, score_rect.centery + 2))

        instruction_rect = instruction_surface.get_rect(
            center=(STATS_WIDTH + MAIN_GAME_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
        instruction_shadow_rect = instruction_shadow_surface.get_rect(
            center=(instruction_rect.centerx + 2, instruction_rect.centery + 2))

        # Blit shadow surfaces followed by text surfaces
        screen.blit(text_shadow_surface, text_shadow_rect)
        screen.blit(text_surface, text_rect)
        screen.blit(score_shadow_surface, score_shadow_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(instruction_shadow_surface, instruction_shadow_rect)
        screen.blit(instruction_surface, instruction_rect)
