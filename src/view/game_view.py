import pygame
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH
from src.view.button_view import Button


class GameView:

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.player_view = None  # Initialized to None
        self.initialize_buttons()

    # Setter for player_view
    def set_player_view(self, player_view):
        self.player_view = player_view

    def render(self, model):
        self.clear_screen()
        self.render_ui()

        # Render player
        if self.player_view:
            self.player_view.render(self.screen)

        self.draw_sprites(model.all_sprites)
        self.display_stats(model)
        pygame.display.flip()

    def clear_screen(self):
        self.screen.fill((0, 0, 0))

    def render_ui(self):
        pygame.draw.rect(self.screen, (200, 200, 200), (0, 0, STATS_WIDTH, SCREEN_HEIGHT))
        for button in self.buttons:
            self.draw_button(button)

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
            ("Power-Up Timer:", self.calculate_time_until_powerup(model.next_powerup_time)),
            ("Average enemy speed:", self.calculate_average_enemy_speed(model.enemies))
        ]

        for i, (text, value) in enumerate(stats):
            stat_surface = self.font.render(f"{text} {value}", True, (0, 0, 0))
            self.screen.blit(stat_surface, (10, 10 + i * 30))

    @staticmethod
    def calculate_time_until_powerup(next_powerup_time):
        current_time = pygame.time.get_ticks()
        return max(0, (next_powerup_time - current_time) // 1000)  # Convert to seconds

    @staticmethod
    def calculate_average_enemy_speed(enemies):
        if len(enemies) > 0:
            total_enemy_speed = sum(enemy.speed for enemy in enemies)
            return total_enemy_speed / len(enemies)
        else:
            return 0
