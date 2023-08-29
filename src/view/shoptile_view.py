import pygame

EXTERNAL_MARGIN = 10
INTERNAL_MARGIN = 10
BORDER_THICKNESS = 2


class ShopTileView:
    def __init__(self, x, y, width, height, model):
        self.rect = pygame.Rect(x, y + 10, width, height)
        self.model = model
        self.color = (100, 100, 100)
        self.hover_color = (150, 150, 150)
        self._initialize_buttons(width)

    def _initialize_buttons(self, width):
        button_width = (width - 2 * INTERNAL_MARGIN - 5) / 2
        self.buy_button = pygame.Rect(self.rect.x + INTERNAL_MARGIN, self.rect.y + self.rect.height - 40, button_width,
                                      30)
        self.sell_button = pygame.Rect(self.rect.x + self.rect.width - INTERNAL_MARGIN - button_width,
                                       self.rect.y + self.rect.height - 40, button_width, 30)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=10, width=BORDER_THICKNESS)
        self._draw_buttons(screen)
        self._draw_texts(screen)

    def _draw_buttons(self, screen):
        buy_hovered = self.buy_button.collidepoint(pygame.mouse.get_pos())
        sell_hovered = self.sell_button.collidepoint(pygame.mouse.get_pos())
        buy_button_color = (0, 128, 0) if not buy_hovered else (0, 100, 0)
        sell_button_color = (255, 0, 0) if not sell_hovered else (139, 0, 0)
        pygame.draw.rect(screen, buy_button_color, self.buy_button, border_radius=5)
        pygame.draw.rect(screen, sell_button_color, self.sell_button, border_radius=5)
        pygame.draw.rect(screen, (255, 255, 255), self.buy_button, border_radius=5, width=2)
        pygame.draw.rect(screen, (255, 255, 255), self.sell_button, border_radius=5, width=2)

        # render the button texts
        button_font = pygame.font.Font(None, 24)
        buy_text_surface = button_font.render("Buy", True, (255, 255, 255))
        sell_text_surface = button_font.render("Sell", True, (255, 255, 255))
        screen.blit(buy_text_surface, (self.buy_button.centerx - buy_text_surface.get_width() // 2,
                                       self.buy_button.centery - buy_text_surface.get_height() // 2))
        screen.blit(sell_text_surface, (self.sell_button.centerx - sell_text_surface.get_width() // 2,
                                        self.sell_button.centery - sell_text_surface.get_height() // 2))

    def _draw_texts(self, screen):
        # Render item title
        title_font = pygame.font.Font(None, 28)
        title_surface = title_font.render(self.model.title, True, (255, 255, 255))
        screen.blit(title_surface, (self.rect.centerx - title_surface.get_width() // 2, self.rect.y + 10))

        # Render item description
        description_font = pygame.font.Font(None, 18)
        wrapped_description = self._wrap_text(self.model.description, description_font,
                                              self.rect.width - 2 * INTERNAL_MARGIN)
        for idx, line in enumerate(wrapped_description):
            description_surface = description_font.render(line, True, (255, 255, 255))
            screen.blit(description_surface, (self.rect.x + INTERNAL_MARGIN, self.rect.y + 50 + idx * 20))

        # Render item price
        price_font = pygame.font.Font(None, 22)
        price_surface = price_font.render(f"Price: {self.model.price} coins", True, (255, 255, 255))
        screen.blit(price_surface, (self.rect.x + INTERNAL_MARGIN, self.rect.y + self.rect.height - 90))

    def _wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        while words:
            line = ''
            while words and font.size(line + words[0])[0] <= max_width:
                line = line + (words.pop(0) + ' ')
            lines.append(line)
        return lines
