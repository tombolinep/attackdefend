import pygame

EXTERNAL_MARGIN = 10
INTERNAL_MARGIN = 10
BORDER_THICKNESS = 2


class ShopTileView:
    WHITE_COLOR = (255, 255, 255)
    FONT_SIZE_24 = 24
    FONT_SIZE_18 = 18
    FONT_SIZE_22 = 22
    FONT_SIZE_28 = 28
    ITEM_TO_ATTRIBUTE_MAP = {
        "Quantum Thrusters": "speed",
        "Energy Shield": "shield",
        "Rapid Charge System": "reload_speed",
        "Dimensional Compression": "diameter",
        "Tractor Beam": "tractor_beam_enabled",
        "Warp Field Generator": "warp_field_enabled",
        "Extra Blaster Mount": "num_of_guns",
        "Rocket Launcher": "rocket_launcher_enabled",
        "Laser Core Upgrade": "laser_enabled",
    }

    def __init__(self, x, y, width, height, model, player):
        self.rect = pygame.Rect(x, y + 10, width, height)
        self.model = model
        self.player = player
        self.color = (100, 100, 100)
        self.hover_color = (150, 150, 150)
        self.checkbox_size = 20
        self.checkbox_spacing = 5
        self.font_24 = pygame.font.Font(None, self.FONT_SIZE_24)
        self.font_18 = pygame.font.Font(None, self.FONT_SIZE_18)
        self.font_22 = pygame.font.Font(None, self.FONT_SIZE_22)
        self.font_28 = pygame.font.Font(None, self.FONT_SIZE_28)
        self._initialize_buttons(width)
        self.status_message_position = (self.buy_button.x + 10, self.buy_button.y - 30)
        self.status_message = None
        self.status_message_color = (255, 255, 255)
        self.status_expires_at = None
        self.checkbox_counts = {}

        self._wrapped_description = self._wrap_text(self.model.description, self.font_18,
                                                    self.rect.width - 2 * INTERNAL_MARGIN)

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
        self._draw_checkboxes(screen, self.player)
        self._draw_status_message(screen)

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
        self._draw_description(screen, self._wrapped_description)
        self._draw_price(screen)

    def _draw_title(self, screen):
        title_font = pygame.font.Font(None, 28)
        title_surface = title_font.render(self.model.title, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.rect.centerx, self.rect.y + 30))
        pygame.draw.line(screen, (255, 255, 255), (title_rect.left, title_rect.bottom),
                         (title_rect.right, title_rect.bottom), 2)
        screen.blit(title_surface, title_rect)

    def _draw_description(self, screen, wrapped_description):
        description_font = pygame.font.Font(None, self.FONT_SIZE_18)
        description_y = self.rect.y + 55

        for idx, line in enumerate(wrapped_description):
            description_surface = description_font.render(line, True, self.WHITE_COLOR)
            text_start_x = self.rect.centerx - description_font.size(line)[0] // 2
            screen.blit(description_surface, (text_start_x, description_y + idx * 20))

    def _draw_price(self, screen):
        price_font = pygame.font.Font(None, 22)
        price_surface = price_font.render(f"Price: {self.model.price} coins", True, (255, 255, 255))
        screen.blit(price_surface, (self.rect.centerx - 50, self.rect.y + self.rect.height - 80))

    def _wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        while words:
            line = words.pop(0)
            while words and font.size(line + ' ' + words[0])[0] <= max_width:
                line += ' ' + words.pop(0)
            lines.append(line)
        return lines

    def _draw_checkboxes(self, screen, player):
        new_checkbox_size = int(self.checkbox_size * 1.5)  # Increase the size by 50%
        new_checkbox_spacing = int(self.checkbox_spacing * 1.5)  # Optionally, increase the spacing by 50% too

        description_font = pygame.font.Font(None, 18)
        wrapped_description = self._wrap_text(self.model.description, description_font,
                                              self.rect.width - 2 * INTERNAL_MARGIN)
        description_height = len(wrapped_description) * 20  # 20 is the line height for the description

        checkbox_start_y = self.rect.y + 55 + description_height + 10  # 55 is the initial Y position for the description, 10 is spacing

        total_checkboxes_width = self.model.limit * new_checkbox_size + (self.model.limit - 1) * new_checkbox_spacing

        center_x = self.rect.x + self.rect.width // 2
        checkbox_start_x = center_x - total_checkboxes_width // 2

        attribute_to_update = self.ITEM_TO_ATTRIBUTE_MAP.get(self.model.title, "")
        attribute_value = player.attributes_bought.get(attribute_to_update, 0)

        for i in range(self.model.limit):
            checkbox_rect = pygame.Rect(
                checkbox_start_x + (new_checkbox_size + new_checkbox_spacing) * i,
                checkbox_start_y,
                new_checkbox_size,
                new_checkbox_size
            )
            pygame.draw.rect(screen, (255, 255, 255), checkbox_rect, 2)  # Draw white outline

            if i < attribute_value:
                pygame.draw.rect(screen, (255, 255, 255), checkbox_rect)

    def set_status_message(self, message, color, button_clicked):
        self.status_message = message
        self.status_message_color = color
        self.status_expires_at = pygame.time.get_ticks() + 2000  # 2 seconds = 2000 milliseconds
        self.last_clicked_button = button_clicked

    def _draw_status_message(self, screen):
        current_time = pygame.time.get_ticks()

        # Check if the status message should be displayed
        if self.status_message and current_time < self.status_expires_at:
            font = pygame.font.SysFont(None, 24)
            text_surface = font.render(self.status_message, True, self.status_message_color)
            if self.last_clicked_button == "buy":
                adjusted_position = (self.buy_button.centerx, self.status_message_position[1] + 18)
            else:
                adjusted_position = (self.sell_button.centerx, self.status_message_position[1] + 18)

            text_rect = text_surface.get_rect()
            text_rect.centerx = adjusted_position[0]
            text_rect.centery = adjusted_position[1]

            screen.blit(text_surface, text_rect.topleft)

        # Remove the status message if its time has expired
        elif self.status_message and current_time >= self.status_expires_at:
            self.status_message = None

    def is_buy_button_clicked(self, pos):
        x, y = pos
        if self.buy_button.collidepoint(x, y):
            return True
        return False

    def update_items_purchased(self, new_quantity, attribute_to_update):
        self.model.attribute_to_update = attribute_to_update

        if new_quantity > self.model.limit or new_quantity < -self.model.limit:  # Added check for negative values
            return
        if isinstance(new_quantity, bool):
            self.items_purchased = new_quantity
            item_type = "boolean"
        elif isinstance(new_quantity, (int, float)):
            self.items_purchased = new_quantity
            item_type = "integer"
        else:
            return

    def update_checkbox(self, attribute, count, player, screen):
        # Get the current value of the attribute from attribute_modifiers
        current_value = player.attributes_bought.get(attribute, None)

        if current_value is None:
            return

        # Check if the current value matches the count; if not, redraw the checkboxes
        if current_value != count:
            self._draw_checkboxes(screen, player)
