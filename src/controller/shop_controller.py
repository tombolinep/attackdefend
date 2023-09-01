import pygame

from src.model.shop import Shop
from src.view.shop_view import ShopView


class ShopController:
    def __init__(self, model, view, screen, event_dispatcher):
        self.model = model
        self.view = view
        self.screen = screen
        self.event_dispatcher = event_dispatcher

    def handle_click(self, pos, player):
        x, y = pos
        for index, item in enumerate(self.view.shop_items):
            if self.view.x + index * 100 <= x <= self.view.x + index * 100 + self.view.width and \
                    self.view.y <= y <= self.view.y + self.view.height:
                if self.model.can_afford_item(item["title"], player):
                    self.model.buy_item(item["title"], player)

    def handle_click(self, pos, player):
        x, y = pos
        for index, item in enumerate(self.model.shop_items):
            if self.view.x + index * 100 <= x <= self.view.x + index * 100 + self.view.width and \
                    self.view.y <= y <= self.view.y + self.view.height:
                if self.model.can_afford_item(item["title"], player):
                    success = self.model.buy_item(item["title"], player)
                    self.event_dispatcher.dispatch_shop_event("shop_item_clicked", item["title"], success)
                    return item["title"], success  # This will be unpacked as powerup_type, purchase_successful
        return None, False  # Return a tuple with None and False when click is not valid

    def open_shop(self, player):
        shop_running = True
        while shop_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    shop_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    powerup_type, purchase_successful = self.handle_click(pos, player)
                    if powerup_type and purchase_successful:
                        self.view.display_purchase_message(self.screen, (100, 100), f"Purchased {powerup_type}!")

            self.view.draw(self.screen, player)

            pygame.display.flip()
