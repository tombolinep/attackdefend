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
        self.checkbox_size = 20
        self.checkbox_spacing = 5

    def _initialize_buttons(self, width):
        button_width = (width - 2 * INTERNAL_MARGIN - 5) / 2
        self.buy_button = pygame.Rect(self.rect.x + INTERNAL_MARGIN + 10, self.rect.y + self.rect.height + 15,
                                      button_width, 30)
        self.sell_button = pygame.Rect(self.rect.x + self.rect.width - INTERNAL_MARGIN - button_width + 13,
                                       self.rect.y + self.rect.height + 15, button_width, 30)

    def draw(self, screen):
        self._draw_rect(screen, self.rect, self.color, BORDER_THICKNESS, 10)
        self._draw_buttons(screen)
        self._draw_texts(screen)
        self._draw_checkboxes(screen)

    def _draw_rect(self, screen, rect, color, width=0, radius=0):
        pygame.draw.rect(screen, color, rect, border_radius=radius, width=width)

    def _draw_buttons(self, screen):
        buttons = [(self.buy_button, (0, 128, 0), (0, 100, 0), "Buy"),
                   (self.sell_button, (255, 0, 0), (139, 0, 0), "Sell")]

        for btn_rect, color, hover_color, text in buttons:
            is_hovered = btn_rect.collidepoint(pygame.mouse.get_pos())
            btn_color = hover_color if is_hovered else color
            self._draw_rect(screen, btn_rect, btn_color, radius=5)
            self._draw_rect(screen, btn_rect, (255, 255, 255), width=2, radius=5)
            self._draw_button_text(screen, btn_rect, text)

    def _draw_button_text(self, screen, rect, text):
        font = pygame.font.Font(None, 24)
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (rect.centerx - text_surface.get_width() // 2,
                                   rect.centery - text_surface.get_height() // 2))

    def _draw_texts(self, screen):
        self._draw_title(screen)
        self._draw_description(screen)
        self._draw_price(screen)

    def _draw_title(self, screen):
        title_font = pygame.font.Font(None, 28)
        title_surface = title_font.render(self.model.title, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.rect.centerx, self.rect.y + 30))
        pygame.draw.line(screen, (255, 255, 255), (title_rect.left, title_rect.bottom),
                         (title_rect.right, title_rect.bottom), 2)
        screen.blit(title_surface, title_rect)

    def _draw_description(self, screen):
        description_font = pygame.font.Font(None, 18)
        wrapped_description = self._wrap_text(self.model.description, description_font,
                                              self.rect.width - 2 * INTERNAL_MARGIN)

        # Calculate total width of each line in the description.
        text_widths = [description_font.size(line)[0] for line in wrapped_description]

        description_y = self.rect.y + 55

        for idx, (line, line_width) in enumerate(zip(wrapped_description, text_widths)):
            description_surface = description_font.render(line, True, (255, 255, 255))

            # Calculate the horizontal starting position for each line.
            center_x = self.rect.x + self.rect.width // 2
            text_start_x = center_x - line_width // 2

            screen.blit(description_surface, (text_start_x, description_y + idx * 20))

    def _draw_price(self, screen):
        price_font = pygame.font.Font(None, 22)
        price_surface = price_font.render(f"Price: {self.model.price} coins", True, (255, 255, 255))
        screen.blit(price_surface, (self.rect.centerx - 50, self.rect.y + self.rect.height - 80))

    def _wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        while words:
            line = ''
            while words and font.size(line + words[0])[0] <= max_width:
                line = line + (words.pop(0) + ' ')
            lines.append(line)
        return lines

    def _draw_checkboxes(self, screen):
        new_checkbox_size = int(self.checkbox_size * 1.5)  # Increase the size by 50%
        new_checkbox_spacing = int(self.checkbox_spacing * 1.5)  # Optionally, increase the spacing by 50% too

        # Calculate the height occupied by the description.
        description_font = pygame.font.Font(None, 18)
        wrapped_description = self._wrap_text(self.model.description, description_font,
                                              self.rect.width - 2 * INTERNAL_MARGIN)
        description_height = len(wrapped_description) * 20  # 20 is the line height for the description

        # Calculate the vertical starting position for the checkboxes
        checkbox_start_y = self.rect.y + 55 + description_height + 10  # 55 is the initial Y position for the description, 10 is spacing

        # Calculate the total width of all checkboxes and the spaces between them
        total_checkboxes_width = self.model.limit * new_checkbox_size + (self.model.limit - 1) * new_checkbox_spacing

        # Calculate the horizontal starting position for the checkboxes
        center_x = self.rect.x + self.rect.width // 2
        checkbox_start_x = center_x - total_checkboxes_width // 2

        for i in range(self.model.limit):
            checkbox_rect = pygame.Rect(
                checkbox_start_x + (new_checkbox_size + new_checkbox_spacing) * i,
                checkbox_start_y,
                new_checkbox_size,
                new_checkbox_size
            )
            pygame.draw.rect(screen, (255, 255, 255), checkbox_rect, 2)  # Draw white outline
