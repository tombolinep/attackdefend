import pygame
from src.shoptile import ShopTile, EXTERNAL_MARGIN, INTERNAL_MARGIN
import time

BACKGROUND_COLOR = (50, 50, 50)
TITLE_COLOR = (255, 255, 255)
BOUGHT_MESSAGE_DURATION = 0.5
INSUFFICIENT_FUNDS_MESSAGE = "Not enough funds!"


class Shop:
    def __init__(self, x, y, width, height, shop_items):
        self.rect = pygame.Rect(x, y, width, height)
        self.shop_items = shop_items
        self.last_message = ""
        self.purchase_successful = False  # Flag to track if the purchase was successful
        self._initialize_tiles(width, height)
        self.selected_tile_index = None
        self.buy_message_position = None
        self.buy_message_end_time = 0

    def _initialize_tiles(self, width, height):
        raw_tile_width = (width - 2 * EXTERNAL_MARGIN - 2 * INTERNAL_MARGIN) // 3
        raw_tile_height = (height - 2 * EXTERNAL_MARGIN - 2 * INTERNAL_MARGIN - 40) // 3
        self.tiles = [self._create_tile(idx, item, raw_tile_width, raw_tile_height) for idx, item in
                      enumerate(self.shop_items)]

    def _create_tile(self, idx, item, tile_width, tile_height):
        row = idx // 3
        col = idx % 3
        tile_x = self.rect.x + EXTERNAL_MARGIN + tile_width * col + INTERNAL_MARGIN * col
        tile_y = self.rect.y + 40 + EXTERNAL_MARGIN + tile_height * row + INTERNAL_MARGIN * row
        return ShopTile(tile_x, tile_y, tile_width, tile_height, item['title'], item['description'], item['price'])

    def _draw_text(self, screen, player):
        title_font = pygame.font.Font(None, 36)
        title_surface = title_font.render("Shop", True, TITLE_COLOR)
        title_x = self.rect.centerx - title_surface.get_width() // 2
        title_y = self.rect.y + 20
        screen.blit(title_surface, (title_x, title_y))

        coin_font = pygame.font.Font(None, 36)
        coin_text = coin_font.render(f"Balance: {player.coins}", True, TITLE_COLOR)
        screen.blit(coin_text, (title_x - 400, title_y))

        message_font = pygame.font.Font(None, 28)
        message_surface = message_font.render(self.last_message, True, TITLE_COLOR)
        screen.blit(message_surface, (self.rect.centerx - message_surface.get_width() // 2, title_y + 40))

    def draw(self, screen, player):
        pygame.draw.rect(screen, BACKGROUND_COLOR, self.rect)
        self._draw_text(screen, player)
        for idx, tile in enumerate(self.tiles):
            tile.draw(screen)
            if self.buy_message_position and self.selected_tile_index == idx and time.time() < self.buy_message_end_time:
                if self.purchase_successful:
                    message = "Bought!"
                    message_color = (0, 255, 0)
                else:
                    message = "Insufficient Funds!"
                    message_color = (255, 0, 0)
                font = pygame.font.Font(None, 36)
                label = font.render(message, 1, message_color)
                screen.blit(label, self.buy_message_position)

    def handle_click(self, pos, player):
        for tile in self.tiles:
            if tile.rect.collidepoint(pos):
                buy_box_rect = tile.get_buy_box_rect()
                self.buy_message_position = (buy_box_rect.centerx, buy_box_rect.y - 30)
                self.buy_message_end_time = time.time() + BOUGHT_MESSAGE_DURATION
                if self.can_buy_item(tile.title, player):
                    self.buy_item(tile.title, player)
                    self.purchase_successful = True
                    self.selected_tile_index = self.tiles.index(tile)
                else:
                    self.purchase_successful = False
                return tile.title
        return None

    def can_buy_item(self, item_title, player):
        item = self.get_item(item_title)
        return item and 0 <= item["price"] <= player.coins

    def buy_item(self, item_title, player):
        item = self.get_item(item_title)
        if item:
            if self.can_buy_item(item_title, player):
                if item["title"] == "Speed Boost":
                    player.increase_speed()
                elif item["title"] == "Coin Bonus":
                    player.coins += 50
                player.coins -= item["price"]
                self.last_message = "Bought!"
            else:
                self.last_message = INSUFFICIENT_FUNDS_MESSAGE

    def get_item(self, item_title):
        for item in self.shop_items:
            if item["title"] == item_title:
                return item
        return None

    def get_buy_box(self, item_title):
        if self.selected_tile_index is not None:
            return self.tiles[self.selected_tile_index]
        return None
