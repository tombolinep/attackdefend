import pygame
from .shoptile import ShopTile, EXTERNAL_MARGIN, INTERNAL_MARGIN

BACKGROUND_COLOR = (50, 50, 50)
TITLE_COLOR = (255, 255, 255)


class Shop:
    def __init__(self, x, y, width, height, shop_items):
        self.rect = pygame.Rect(x, y, width, height)
        self.shop_items = shop_items

        # Tile dimensions
        raw_tile_width = (width - 2 * EXTERNAL_MARGIN - 2 * INTERNAL_MARGIN) // 3
        raw_tile_height = (height - 2 * EXTERNAL_MARGIN - 2 * INTERNAL_MARGIN - 40) // 3

        # Initialize tiles in a 3x3 grid
        self.tiles = []
        for idx, item in enumerate(shop_items):
            row = idx // 3
            col = idx % 3

            tile_x = x + EXTERNAL_MARGIN + raw_tile_width * col + INTERNAL_MARGIN * col
            tile_y = y + 40 + EXTERNAL_MARGIN + raw_tile_height * row + INTERNAL_MARGIN * row  # 40 for the title
            self.tiles.append(
                ShopTile(tile_x, tile_y, raw_tile_width, raw_tile_height, item['title'], item['description'],
                         item['price']))

    def draw(self, screen):
        pygame.draw.rect(screen, BACKGROUND_COLOR, self.rect)

        title_font = pygame.font.Font(None, 36)
        title_surface = title_font.render("Shop", True, TITLE_COLOR)
        title_position = (self.rect.centerx - title_surface.get_width() // 2, self.rect.y + 20)
        screen.blit(title_surface, title_position)

        for tile in self.tiles:
            tile.draw(screen)

    def handle_click(self, pos, player_score):
        for tile in self.tiles:
            if tile.is_hovered(pos) and player_score >= tile.price:
                return tile.title
        return None
