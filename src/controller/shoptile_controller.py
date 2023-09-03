class ShopTileController:
    def __init__(self, model, view, event_dispatcher, shop_model):
        self.model = model
        self.view = view
        self.event_dispatcher = event_dispatcher
        self.shop_model = shop_model

    def handle_click(self, pos, player, item_title):
        if self.view.buy_button.collidepoint(pos):
            if self.can_afford_item(item_title, player):
                self.view.set_status_message("Bought!", (0, 255, 0))
                self.event_dispatcher.dispatch_event("buy_item", {"title": self.model.title, "price": self.model.price})
            else:
                self.view.set_status_message("Cannot afford", (255, 0, 0))
            return True
        return False

    def can_afford_item(self, item_title, player):
        item = self.get_item(item_title)
        return item and 0 <= item["price"] <= player.coins

    def get_item(self, item_title):
        return self.shop_model.get_item(item_title)
