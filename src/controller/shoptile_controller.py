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

    def handle_click(self, pos, player, item_title):
        print(f"Item title received: {repr(item_title)}")  # Debug line
        print(f"Available items: {self.ITEM_TO_ATTRIBUTE_MAP.keys()}")  # Debug line

        item_price = self.get_item(item_title).get('price', 0)
        attribute_to_update = self.ITEM_TO_ATTRIBUTE_MAP.get(item_title, None)

        if attribute_to_update is None:
            self.view.set_status_message("Unknown Item", (255, 0, 0), "error")
            return False

        if self.view.buy_button.collidepoint(pos):
            if self.can_afford_item(item_title, player):
                player.add_coin(-item_price)

                current_value = getattr(player, attribute_to_update)
                if isinstance(current_value, int):
                    setattr(player, attribute_to_update, current_value + 1)
                elif isinstance(current_value, bool):
                    setattr(player, attribute_to_update, True)
                self.view.set_status_message("Bought!", (0, 255, 0), "buy")
                return True
            else:
                self.view.set_status_message("Cannot afford", (255, 0, 0), "buy")
                return True

        elif self.view.sell_button.collidepoint(pos):
            if player.can_sell_item(attribute_to_update, 1):
                current_value = getattr(player, attribute_to_update)
                if isinstance(current_value, int):
                    setattr(player, attribute_to_update, current_value - 1)
                elif isinstance(current_value, bool):
                    setattr(player, attribute_to_update, False)
                player.add_coin(item_price)
                self.view.set_status_message("Sold!", (0, 255, 0), "sell")
                return True
            else:
                self.view.set_status_message("Cannot sell", (255, 0, 0), "sell")
                return True
        return False

    def can_afford_item(self, item_title, player):
        item = self.get_item(item_title)
        return item and 0 <= item["price"] <= player.coins

    def get_item(self, item_title):
        return self.shop_model.get_item(item_title)
