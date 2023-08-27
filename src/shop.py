import pygame

# Colors, Fonts, and other constants for the shop
BACKGROUND_COLOR = (50, 50, 50)
BORDER_COLOR = (200, 200, 200)
TITLE_COLOR = (255, 255, 255)
EXTERNAL_MARGIN = 10  # margin between tiles and the shop window
INTERNAL_MARGIN = 5  # margin between tiles


class ShopTile:
    def __init__(self, x, y, width, height, powerup_type, price):
        self.rect = pygame.Rect(x, y, width, height)
        self.powerup_type = powerup_type
        self.price = price
        self.color = (100, 100, 100)
        self.hover_color = (150, 150, 150)

    def draw(self, screen):
        color = self.hover_color if self.is_hovered(pygame.mouse.get_pos()) else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        # You can also add text to display price, powerup name etc.

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)


class Shop:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

        # Raw tile dimensions
        raw_tile_width = (width - 2 * EXTERNAL_MARGIN - 2 * INTERNAL_MARGIN) // 3
        raw_tile_height = (height - 2 * EXTERNAL_MARGIN - 2 * INTERNAL_MARGIN - 40) // 3

        # Adjust for 20% smaller size
        tile_width = int(raw_tile_width * 0.8)
        tile_height = int(raw_tile_height * 0.8)

        # Calculate total width and height occupied by all tiles
        total_tiles_width = 3 * tile_width + 2 * INTERNAL_MARGIN
        total_tiles_height = 3 * tile_height + 2 * INTERNAL_MARGIN

        # Additional offset to center the entire 3x3 grid within the shop
        center_offset_x = (width - total_tiles_width) // 2
        center_offset_y = (height - 40 - total_tiles_height) // 2

        # Initialize tiles in a 3x3 grid
        self.tiles = []
        for row in range(3):
            for col in range(3):
                tile_x = x + center_offset_x + (tile_width + INTERNAL_MARGIN) * col
                tile_y = y + 40 + center_offset_y + (tile_height + INTERNAL_MARGIN) * row  # 40 for the title
                self.tiles.append(ShopTile(tile_x, tile_y, tile_width, tile_height, f"PowerUp{len(self.tiles) + 1}",
                                           (len(self.tiles) + 1) * 100))

    def draw(self, screen):
        # Draw background
        pygame.draw.rect(screen, BACKGROUND_COLOR, self.rect)

        # Draw title
        title_font = pygame.font.Font(None, 52)
        title_surface = title_font.render("Shop", True, TITLE_COLOR)
        title_position = (self.rect.centerx - title_surface.get_width() // 2, self.rect.y + 75)
        screen.blit(title_surface, title_position)

        # Draw tiles
        for tile in self.tiles:
            tile.draw(screen)

    def handle_click(self, pos, player_score):
        for tile in self.tiles:
            if tile.is_hovered(pos):
                if player_score >= tile.price:
                    return tile.powerup_type
        return None
