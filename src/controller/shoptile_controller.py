from src.controller.shop_controller import ShopController


class ShopTileController:
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

    def __init__(self, model, view, event_dispatcher, shop_model):
        self.model = model
        self.view = view
        self.event_dispatcher = event_dispatcher
        self.shop_model = shop_model

    def handle_click(self, pos, player, item_title, action):
        print(f"Item title received: {repr(item_title)}")

        item_price = self.get_item_price(item_title)
        attribute_to_update = self.get_attribute_to_update(item_title)

        if attribute_to_update is None:
            self.view.set_status_message("Unknown Item", (255, 0, 0), "error")
            return False

        if action == ShopController.ACTION_BUY:
            return self.handle_buy(player, item_title, item_price, attribute_to_update)
        elif action == ShopController.ACTION_SELL:
            return self.handle_sell(player, item_title, item_price, attribute_to_update)
        return False

    def handle_buy(self, player, item_title, item_price, attribute_to_update):
        if self.can_afford_item(item_title, player):
            player.add_coin(-item_price)
            self.update_player_attribute(player, attribute_to_update, increment=True)
            self.view.set_status_message("Bought!", (0, 255, 0), "buy")
            return True
        else:
            self.view.set_status_message("Cannot afford", (255, 0, 0), "buy")
            return True

    def handle_sell(self, player, item_title, item_price, attribute_to_update):
        if player.can_sell_item(attribute_to_update, 1):
            self.update_player_attribute(player, attribute_to_update, increment=False)
            player.add_coin(item_price)
            self.view.set_status_message("Sold!", (0, 255, 0), "sell")
            return True
        else:
            self.view.set_status_message("Cannot sell", (255, 0, 0), "sell")
            return True

    def update_player_attribute(self, player, attribute, increment):
        current_value = getattr(player, attribute)
        new_value = current_value + 1 if increment and isinstance(current_value, int) else current_value
        new_value = current_value - 1 if not increment and isinstance(current_value, int) else new_value
        new_value = True if increment and isinstance(current_value, bool) else new_value
        new_value = False if not increment and isinstance(current_value, bool) else new_value
        setattr(player, attribute, new_value)

    def get_item_price(self, item_title):
        return self.get_item(item_title).get('price', 0)

    def get_attribute_to_update(self, item_title):
        return self.ITEM_TO_ATTRIBUTE_MAP.get(item_title, None)

    def can_afford_item(self, item_title, player):
        item = self.get_item(item_title)
        return item and 0 <= item["price"] <= player.coins

    def get_item(self, item_title):
        return self.shop_model.get_item(item_title)
