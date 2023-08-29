import pygame
from src.events import EventDispatcher


class ShopController:
    def __init__(self, model, view, event_dispatcher):
        self.model = model
        self.view = view
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
        for index, item in enumerate(self.view.shop_items):
            if self.view.x + index * 100 <= x <= self.view.x + index * 100 + self.view.width and \
                    self.view.y <= y <= self.view.y + self.view.height:
                if self.model.can_afford_item(item["title"], player):
                    success = self.model.buy_item(item["title"], player)
                    self.event_dispatcher.dispatch_shop_event("shop_item_clicked", item["title"], success)
                    
    def open_shop(self, screen, player):
        shop_running = True

        while shop_running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    powerup_type, purchase_successful = self.model.handle_purchase(pygame.mouse.get_pos(), player)
                    if powerup_type and purchase_successful:
                        self.view.display_purchase_message(screen, (100, 100), f"Purchased {powerup_type}!")
                        return powerup_type  # or some other handling
