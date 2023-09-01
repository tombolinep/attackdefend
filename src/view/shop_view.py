import pygame

from src.constants import MAIN_GAME_WIDTH, STATS_WIDTH, SCREEN_HEIGHT
from src.controller.shoptile_controller import ShopTileController
from src.model.shoptile import ShopTile
from src.view.shoptile_view import ShopTileView


class ShopView:
    def __init__(self, model, game_controller):
        self.model = model
        self.game_controller = game_controller

        main_game_width = MAIN_GAME_WIDTH

        self.width = int(main_game_width * 0.7)
        self.height = int(SCREEN_HEIGHT * 0.85)

        self.x = (main_game_width - self.width) // 2 + STATS_WIDTH

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
            tile_model = ShopTile(item['title'], item['description'], item['price'])
            tile_view = ShopTileView(tile_x, tile_y, self.tile_width, self.tile_height, tile_model)
            tile_controller = ShopTileController(tile_model, tile_view)
            self.tiles.append((tile_model, tile_view, tile_controller))

    def draw(self, screen, player):
        num_rows = -(-len(self.tiles) // 3)
        total_height = self.y + 60 + num_rows * self.tile_height + self.buffer * 2

        pygame.draw.rect(screen, (50, 50, 50), (self.x, self.y, self.width, total_height - self.y))

        pygame.draw.rect(screen, (150, 150, 150), (self.x, self.y, self.width, total_height - self.y), 5)

        title_font = pygame.font.Font(None, 36)

        balance_text = f"Balance: {player.coins}"
        balance_surface = title_font.render(balance_text, True, (255, 255, 255))
        screen.blit(balance_surface, (self.x + 20, self.y + 20))

        title_text = "Shop"
        title_surface = title_font.render(title_text, True, (255, 255, 255))
        title_x = self.x + self.width // 2 - title_surface.get_width() // 2
        screen.blit(title_surface, (title_x, self.y + 20))

        close_text = "[close]"
        close_surface = title_font.render(close_text, True, (255, 255, 255))
        close_x = self.x + self.width - close_surface.get_width() - 20
        screen.blit(close_surface, (close_x, self.y + 20))

        tile_start_y = self.y + 60 + self.buffer
        tile_start_x = self.x + self.buffer

        for index, (tile_model, tile_view, tile_controller) in enumerate(self.tiles):
            tile_y = tile_start_y + (index // 3) * self.tile_height
            tile_x = tile_start_x + (index % 3) * self.tile_width
            tile_view.rect.y = tile_y
            tile_view.rect.x = tile_x
            tile_view.draw(screen)

    def create_shop_window(self, screen, shop_items):
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width * len(shop_items), self.height))

    def create_shop_button(self, screen, item, index):
        pygame.draw.rect(screen, (0, 0, 0), (self.x + index * 100, self.y, self.width, self.height))
        text = pygame.font.SysFont('Arial', 20).render(item['title'], True, (0, 0, 0))
        screen.blit(text, (self.x + index * 100 + 15, self.y + 25))

    def display_purchase_message(self, screen, position, message):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 30)
        text_surface = font.render(message, True, (255, 255, 255))
        screen.blit(text_surface, position)
