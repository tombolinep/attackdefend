import pygame

EXTERNAL_MARGIN = 10  # margin between tiles and the shop window
INTERNAL_MARGIN = 10  # margin between tiles
BORDER_THICKNESS = 2  # Border thickness for all tiles


class ShopTile:
    def __init__(self, x, y, width, height, title, description, price):
        y_offset = 10
        self.rect = pygame.Rect(x, y + y_offset, width, height)
        self.title = title
        self.description = description
        self.price = price
        self.color = (100, 100, 100)
        self.hover_color = (150, 150, 150)

        button_gap = 5
        button_margin = 5  # Adjust this value as needed for the distance from the bottom

        button_width = (width - 2 * INTERNAL_MARGIN - button_gap) / 2

        self.buy_button = pygame.Rect(self.rect.x + INTERNAL_MARGIN,
                                      self.rect.y + self.rect.height - 35 - button_margin,
                                      button_width, 30)
        self.sell_button = pygame.Rect(self.rect.x + self.rect.width - INTERNAL_MARGIN - button_width,
                                       self.rect.y + self.rect.height - 35 - button_margin,
                                       button_width, 30)

    def draw(self, screen):
        # Draw the main tile
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10, width=BORDER_THICKNESS)

        # Check for hover on the buttons individually
        buy_hovered = self.buy_button.collidepoint(pygame.mouse.get_pos())
        sell_hovered = self.sell_button.collidepoint(pygame.mouse.get_pos())

        # Decide colors based on hover
        buy_button_color = (0, 128, 0) if not buy_hovered else (0, 100, 0)  # green/darkgreen
        sell_button_color = (255, 0, 0) if not sell_hovered else (139, 0, 0)  # red/darkred

        pygame.draw.rect(screen, buy_button_color, self.buy_button)
        pygame.draw.rect(screen, sell_button_color, self.sell_button)

        # Draw the title text
        title_font = pygame.font.Font(None, 24)
        title_surface = title_font.render(self.title, True, (255, 255, 255))
        title_x = self.rect.x + (self.rect.width - title_surface.get_width()) // 2  # Centering the title
        title_position = (title_x, self.rect.y + 10)
        screen.blit(title_surface, title_position)

        # Draw the price text directly below the title
        price_font = pygame.font.Font(None, 18)
        price_surface = price_font.render(f"${self.price}", True, (255, 255, 255))
        price_x = self.rect.x + (self.rect.width - price_surface.get_width()) // 2
        price_y = title_position[1] + title_surface.get_height() + 5
        screen.blit(price_surface, (price_x, price_y))

        # Title border
        title_border_rect = pygame.Rect(self.rect.x,
                                        self.rect.y,
                                        self.rect.width,
                                        price_y - self.rect.y + price_surface.get_height() + 2 * INTERNAL_MARGIN)
        pygame.draw.rect(screen, self.color, title_border_rect, border_radius=10, width=BORDER_THICKNESS)

        # Draw the description text with border
        description_font = pygame.font.Font(None, 24)
        description_surface = description_font.render(self.description, True, (200, 200, 200))
        desc_start_y = self.rect.y + self.rect.height * 0.5 + 10  # Adding a vertical offset
        description_position = (self.rect.x + 10, desc_start_y + 10)
        screen.blit(description_surface, description_position)

        # Description border
        border_rect = pygame.Rect(self.rect.x, desc_start_y,
                                  self.rect.width - 2, (self.rect.height * 0.3))
        pygame.draw.rect(screen, self.color, border_rect, border_radius=10,
                         width=BORDER_THICKNESS)  # '2' is the border thickness

        # Text for buy and sell buttons
        button_font = pygame.font.Font(None, 24)
        buy_text = button_font.render("Buy", True, (255, 255, 255))
        buy_text_position = (self.buy_button.x + (self.buy_button.width - buy_text.get_width()) // 2,
                             self.buy_button.y + (self.buy_button.height - buy_text.get_height()) // 2)
        screen.blit(buy_text, buy_text_position)

        sell_text = button_font.render("Sell", True, (255, 255, 255))
        sell_text_position = (self.sell_button.x + (self.sell_button.width - sell_text.get_width()) // 2,
                              self.sell_button.y + (self.sell_button.height - sell_text.get_height()) // 2)
        screen.blit(sell_text, sell_text_position)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

        # Text for buy and sell buttons
        button_font = pygame.font.Font(None, 24)
        buy_text = button_font.render("Buy", True, (255, 255, 255))
        buy_text_position = (self.buy_button.x + (self.buy_button.width - buy_text.get_width()) // 2,
                             self.buy_button.y + (self.buy_button.height - buy_text.get_height()) // 2)
        screen.blit(buy_text, buy_text_position)

        sell_text = button_font.render("Sell", True, (255, 255, 255))
        sell_text_position = (self.sell_button.x + (self.sell_button.width - sell_text.get_width()) // 2,
                              self.sell_button.y + (self.sell_button.height - sell_text.get_height()) // 2)
        screen.blit(sell_text, sell_text_position)
