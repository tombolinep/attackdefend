import pygame


class ShopTileController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def handle_click(self, pos):
        if self.view.buy_button.collidepoint(pos):
            return 'buy', self.model.title, self.model.price
        elif self.view.sell_button.collidepoint(pos):
            return 'sell', self.model.title, self.model.price
        return None, None, None
