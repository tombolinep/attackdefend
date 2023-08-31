import pygame


class EventDispatcher:
    def __init__(self):
        self.listeners = {}
        self.shop_tile_controllers = []  # A list to store all the ShopTileController instances
        self.view = None

    def add_listener(self, event_name, callback):
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    def remove_listener(self, event_name, callback):
        if event_name in self.listeners:
            self.listeners[event_name].remove(callback)

    def dispatch_event(self, event_name, data=None):
        if event_name in self.listeners:
            for callback in self.listeners[event_name]:
                callback(data)

    def add_shop_tile_controller(self, controller):
        self.shop_tile_controllers.append(controller)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            for controller in self.shop_tile_controllers:
                action, title, price = controller.handle_click(pos)

                if action == 'buy':
                    self.dispatch_event("buy_item", {"title": title, "price": price})
                elif action == 'sell':
                    self.dispatch_event("sell_item", {"title": title, "price": price})
                elif self.is_pause_button_clicked(pos):
                    self.dispatch_event("pause_game")

    def dispatch_button_click(self, mouse_pos):
        if self.view.pause_button.is_clicked(mouse_pos):
            self.fire_event("pause_game")
