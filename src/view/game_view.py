import pygame
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH, MAIN_GAME_WIDTH, BULLET_INTERVAL
from src.view.button_view import Button
from src.utils import resource_path


class GameView:

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.player_view = None  # Initialized to None
        self.initialize_buttons()
        self.background_image = pygame.image.load(resource_path('assets/space_background.jpg'))
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background_x_pos = 0

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

        # Update the x-coordinate for scrolling
        self.background_x_pos -= 0.1
        if self.background_x_pos <= -SCREEN_WIDTH:
            self.background_x_pos = 0

    def clear_screen(self):
        # Blit the background image twice to create a scrolling effect
        self.screen.blit(self.background_image, (self.background_x_pos, 0))
        self.screen.blit(self.background_image, (self.background_x_pos + SCREEN_WIDTH, 0))

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
        mouse_pos = pygame.mouse.get_pos()
        if button.rect.collidepoint(mouse_pos):
            button.color = button.hover_color
        else:
            button.color = button.normal_color

        button_rect = button.rect
        pygame.draw.rect(self.screen, button.color, button_rect)
        text_surface = self.font.render(button.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_sprites(self, sprites):
        for entity in sprites:
            if hasattr(entity, 'surf'):
                self.screen.blit(entity.surf, entity.rect)

    def initialize_buttons(self):
        common_button_color = (150, 150, 150)
        common_button_hover_color = (200, 200, 200)

        self.pause_button = Button(SCREEN_WIDTH - 150, 10, 130, 40, "Pause", common_button_color,
                                   common_button_hover_color)
        self.shop_button = Button(SCREEN_WIDTH - 150, 60, 130, 40, "Shop", common_button_color,
                                  common_button_hover_color)
        self.buttons = [self.pause_button, self.shop_button]

    def display_stats(self, model):

        rapid_charge_system_count = model.player.attributes_bought.get('reload_speed', 0)
        adjusted_bullet_interval = BULLET_INTERVAL - (500 * rapid_charge_system_count)
        time_per_shot_in_seconds = adjusted_bullet_interval / 1000

        stats = [
            ("Score:", int(model.score)),
            ("Coins:", model.player.coins),
            ("", ""),
            ("Enemy speed:", model.calculate_average_enemy_speed(model.enemies)),
            ("", ""),
            ("Speed:", model.player.speed),
            ("Size:", model.player.diameter),
            ("Shield:", model.player.shield),
            ("Fire Rate:", round(time_per_shot_in_seconds, 2)),
            ("Number of Guns:", model.player.num_of_guns),
            ("Tractor Beam:", "True" if model.player.tractor_beam_enabled else "False"),
            ("Warp Field:", "True" if model.player.warp_field_enabled else "False"),
            ("Rocket Launcher:", "True" if model.player.rocket_launcher_enabled else "False"),
            ("Laser:", "True" if model.player.laser_enabled else "False"),
        ]

        header_font = pygame.font.Font(None, 32)  # Adjust font size for headers
        value_font = pygame.font.Font(None, 32)  # Adjust font size for values

        for i, (text, value) in enumerate(stats):
            if text:
                font = header_font if ":" in text else value_font
                color = (0, 0, 0) if ":" in text else (0, 0, 139)  # Dark blue for values
                text_surface = font.render(text, True, color)
                value_surface = font.render(f"{value}", True, (0, 0, 139))  # Dark blue for values
                self.screen.blit(text_surface, (10, 10 + i * 30))
                self.screen.blit(value_surface, (220, 10 + i * 30))  # Adjust x-value for alignment
            else:
                continue
