class ShopTileController:
    def __init__(self, model, view, event_dispatcher):
        self.model = model
        self.view = view
        self.event_dispatcher = event_dispatcher

    def handle_click(self, pos):
        if self.view.is_buy_button_clicked(pos):
            self.event_dispatcher.dispatch_event("buy_item", {"title": self.model.title, "price": self.model.price})
            return "buy", self.model.title, self.model.price
        elif self.view.is_sell_button_clicked(pos):
            self.event_dispatcher.dispatch_event("sell_item", {"title": self.model.title, "price": self.model.price})
            return "sell", self.model.title, self.model.price
        return None, None, None
