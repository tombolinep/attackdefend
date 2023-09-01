import pygame
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH, MAIN_GAME_WIDTH
from src.view.button_view import Button
from src.view.shop_view import ShopView


class GameView:

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.player_view = None  # Initialized to None
        self.initialize_buttons()

    def set_player_view(self, player_view):
        self.player_view = player_view

    def render(self, model):
        self.clear_screen()
        self.render_ui(model)

        # Render player
        if self.player_view:
            self.player_view.render(self.screen)

        self.draw_sprites(model.all_sprites)
        self.display_stats(model)
        pygame.display.flip()

    def clear_screen(self):
        self.screen.fill((0, 0, 0))

    def render_ui(self, model):
        pygame.draw.rect(self.screen, (200, 200, 200), (0, 0, STATS_WIDTH, SCREEN_HEIGHT))
        self.update_button_texts(model)
        for button in self.buttons:
            self.draw_button(button)

    def update_button_texts(self, model):
        for button in self.buttons:
            if button.text == "Pause" or button.text == "Resume":
                button.text = "Resume" if model.paused else "Pause"

    def draw_button(self, button):
        button_rect = button.rect
        pygame.draw.rect(self.screen, button.color, button_rect)
        text_surface = self.font.render(button.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_sprites(self, sprites):
        for entity in sprites:
            if hasattr(entity, 'surf'):  # Check if the sprite has a 'surf' attribute
                self.screen.blit(entity.surf, entity.rect)

    def initialize_buttons(self):
        self.pause_button = Button(SCREEN_WIDTH - 150, 10, 130, 40, "Pause", (150, 150, 150), (200, 200, 200))
        self.shop_button = Button(SCREEN_WIDTH - 150, 60, 130, 40, "Shop", (150, 150, 150), (200, 200, 200))
        self.buttons = [self.pause_button, self.shop_button]

    def display_stats(self, model):
        stats = [
            ("Score:", int(model.score)),
            ("Your speed:", model.player.speed),
            ("Coins:", model.player.coins),
            ("Power-Up Timer:", model.calculate_time_until_powerup(model.next_powerup_time)),
            ("Average enemy speed:", model.calculate_average_enemy_speed(model.enemies))
        ]

        for i, (text, value) in enumerate(stats):
            stat_surface = self.font.render(f"{text} {value}", True, (0, 0, 0))
            self.screen.blit(stat_surface, (10, 10 + i * 30))

    def display_game_over(self):
        font = pygame.font.Font(None, 74)
        text_surface = font.render('Game Over', True, (255, 0, 0))

        text_rect = text_surface.get_rect(center=(STATS_WIDTH + MAIN_GAME_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))

        instruction_font = pygame.font.Font(None, 36)
        instruction_surface = instruction_font.render('Press R to Retry or Q to Quit', True, (255, 255, 255))

        instruction_rect = instruction_surface.get_rect(
            center=(STATS_WIDTH + MAIN_GAME_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))

        self.screen.blit(text_surface, text_rect)
        self.screen.blit(instruction_surface, instruction_rect)

        pygame.display.flip()
