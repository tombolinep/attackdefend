import pygame

from constants import MAIN_GAME_WIDTH, STATS_WIDTH, SCREEN_HEIGHT
from controller.shoptile_controller import ShopTileController
from model.shoptile import ShopTile
from view.button_view import Button
from view.shoptile_view import ShopTileView


class ShopView:
    def __init__(self, model, game_controller, event_dispatcher):
        self.model = model
        self.game_controller = game_controller
        self.event_dispatcher = event_dispatcher

        self.width = int(MAIN_GAME_WIDTH * 0.7)
        self.height = int(SCREEN_HEIGHT * 0.85)

        self.x = (MAIN_GAME_WIDTH - self.width) // 2 + STATS_WIDTH
        self.y = (SCREEN_HEIGHT - self.height) // 4

        self.tile_width = self.width // 3
        self.tile_height = self.height // 3
        self.buffer = 10

        self.tile_width = (self.width - self.buffer * 2) // 3
        self.tile_height = (self.height - self.buffer * 2) // 3

        self.tiles = []
        for index, item in enumerate(self.model.shop_items):
            tile_x = self.x + (index % 3) * self.tile_width
            tile_y = self.y + (index // 3) * self.tile_height
            tile_model = ShopTile(item['title'], item['description'], item['price'], item['limit'])
            tile_view = ShopTileView(tile_x, tile_y, self.tile_width, self.tile_height, tile_model, self.model.player)
            tile_controller = ShopTileController(tile_model, tile_view, self.event_dispatcher, self.model,
                                                 self.model.audio_manager)
            self.tiles.append((tile_model, tile_view, tile_controller))

        close_button_width = 130
        close_button_height = 40

        close_button_x = self.x + self.width - close_button_width - 20
        close_button_y = self.y + 20

        button_color = (50, 50, 50)
        button_hover_color = (75, 75, 75)

        self.close_button = Button(close_button_x, close_button_y, close_button_width, close_button_height, "[Close]",
                                   button_color, button_hover_color)

        self.messages = []

    def draw(self, screen, player):
        num_rows = -(-len(self.tiles) // 3)
        total_height = self.y + 60 + num_rows * self.tile_height + self.buffer * 2

        pygame.draw.rect(screen, (50, 50, 50), (self.x, self.y, self.width, total_height - self.y))
        pygame.draw.rect(screen, (150, 150, 150), (self.x, self.y, self.width, total_height - self.y), 5)

        title_font = pygame.font.Font(None, 36)

        # Calculate common Y position for Balance, Shop, and Close Button
        common_y = self.y + 20

        balance_text = f"Balance: {player.coins}"
        balance_surface = title_font.render(balance_text, True, (255, 255, 255))
        screen.blit(balance_surface, (self.x + 20, common_y))

        title_text = "Shop"
        title_surface = title_font.render(title_text, True, (255, 255, 255))
        title_x = self.x + self.width // 2 - title_surface.get_width() // 2
        screen.blit(title_surface, (title_x, common_y))

        self.close_button.rect.y = common_y - 10  # Adjust for button height
        self.close_button.draw(screen)

        tile_start_y = self.y + 60 + self.buffer
        tile_start_x = self.x + self.buffer

        for index, (tile_model, tile_view, tile_controller) in enumerate(self.tiles):
            tile_y = tile_start_y + (index // 3) * self.tile_height
            tile_x = tile_start_x + (index % 3) * self.tile_width
            tile_view.rect.y = tile_y
            tile_view.rect.x = tile_x
            tile_view.draw(screen)
