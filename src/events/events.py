import pygame


class EventDispatcher:
    def __init__(self):
        self.listeners = {}
        self.shop_tile_controllers = []  # A list to store all the ShopTileController instances

    def add_listener(self, event_name, callback):
        """Add a listener for a specific event."""
        if event_name not in self.listeners:
            self.listeners[event_name] = []
        self.listeners[event_name].append(callback)

    def remove_listener(self, event_name, callback):
        """Remove a specific listener for a specific event."""
        if event_name in self.listeners:
            self.listeners[event_name].remove(callback)

    def dispatch_event(self, event_name, data=None):
        """Dispatch an event to all listeners for that event."""
        if event_name in self.listeners:
            for callback in self.listeners[event_name]:
                callback(data)

    def add_shop_tile_controller(self, controller):
        """Add a ShopTileController to the dispatcher."""
        self.shop_tile_controllers.append(controller)

    def handle_event(self, event):
        """Handle events including shop tile clicks."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            for controller in self.shop_tile_controllers:
                action, title, price = controller.handle_click(pos)

                if action == 'buy':
                    self.dispatch_event("buy_item", {"title": title, "price": price})
                elif action == 'sell':
                    self.dispatch_event("sell_item", {"title": title, "price": price})
