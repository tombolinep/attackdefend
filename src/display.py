import pygame
from pygame.locals import KEYDOWN, QUIT
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH, MAIN_GAME_WIDTH


class Display:
    @staticmethod
    def display_stats(screen, score, player_speed, average_enemy_speed):
        font = pygame.font.SysFont(None, 36)

        score_surface = font.render(f"Score: {int(score)}", True, (0, 0, 0))
        player_speed_surface = font.render(f"Your speed: {player_speed}", True, (0, 0, 0))
        average_enemy_speed_surface = font.render(f"Avg speed: {average_enemy_speed:.2f}", True, (0, 0, 0))

        screen.blit(score_surface, (10, 10))
        screen.blit(player_speed_surface, (10, 40))
        screen.blit(average_enemy_speed_surface, (10, 70))

    @staticmethod
    def display_game_over(screen):
        font = pygame.font.Font(None, 74)
        text_surface = font.render('Game Over', True, (255, 0, 0))

        text_rect = text_surface.get_rect(center=(STATS_WIDTH + MAIN_GAME_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))

        instruction_font = pygame.font.Font(None, 36)
        instruction_surface = instruction_font.render('Press R to Retry or Q to Quit', True, (255, 255, 255))

        instruction_rect = instruction_surface.get_rect(
            center=(STATS_WIDTH + MAIN_GAME_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))

        screen.blit(text_surface, text_rect)
        screen.blit(instruction_surface, instruction_rect)

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == pygame.K_r:  # Retry
                        return True
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:  # Quit
                        return False
                elif event.type == QUIT:
                    return False
