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

            new_quantity = player.attribute_modifiers.get(attribute_to_update)

            # Update the view to reflect the new model state, only for integer attributes
            if isinstance(new_quantity, int):
                self.view.update_items_purchased(new_quantity, attribute_to_update)

            self.view.set_status_message("Bought!", (0, 255, 0), "buy")
            return True
        else:
            self.view.set_status_message("Cannot afford", (255, 0, 0), "buy")
            return False

    def handle_sell(self, player, item_title, item_price, attribute_to_update):
        if player.can_sell_item(attribute_to_update, 1):
            # Determine the current modifier and adjust it to handle the sale
            current_modifier = player.attribute_modifiers.get(attribute_to_update)

            if isinstance(current_modifier, bool):
                new_modifier = False
            else:
                new_modifier = max(0, current_modifier - 1)

            # Update the attribute modifier in the player's data structure
            player.attribute_modifiers[attribute_to_update] = new_modifier

            # Adjust the player's coin balance to reflect the sale
            player.add_coin(int(item_price * 0.7))

            # Update the player's attribute to reflect the change in modifiers
            player.update_attribute(attribute_to_update, -1 if not isinstance(new_modifier, bool) else False)

            # Set the Player's attribute to the effective value after applying the modifier
            setattr(player, attribute_to_update, player.get_effective_attribute(attribute_to_update))

            # Update the view to show the new state of items purchased
            new_quantity = player.attribute_modifiers[attribute_to_update]

            # Update the view to reflect the new model state, only for integer attributes
            if isinstance(new_quantity, int):
                self.view.update_items_purchased(new_quantity, attribute_to_update)

            self.view.set_status_message("Sold!", (0, 255, 0), "sell")
            return True
        else:
            self.view.set_status_message("Cannot sell", (255, 0, 0), "sell")
            return False

    def update_player_attribute(self, player, attribute_to_update, increment=True):
        # Get the base value and the modifier
        base_value = player.ATTRIBUTE_DEFAULTS.get(attribute_to_update)
        modifier = player.attribute_modifiers.get(attribute_to_update)

        # Determine the new value based on the attribute type
        if isinstance(base_value, bool):
            new_value = True
        else:
            # For integer attributes, calculate the new value based on the modifier
            new_value = base_value + modifier
            if increment:
                new_value += 1
            else:
                new_value = max(base_value, new_value - 1)  # Ensure the value doesn't go below the default

        # Update both the attribute and the modifier
        setattr(player, attribute_to_update, new_value)
        player.attribute_modifiers[attribute_to_update] = new_value - base_value

    def get_item_price(self, item_title):
        return self.get_item(item_title).get('price', 0)

    def get_attribute_to_update(self, item_title):
        return self.ITEM_TO_ATTRIBUTE_MAP.get(item_title, None)

    def get_attribute_count(self, player, attribute):
        current_value = getattr(player, attribute)
        if isinstance(current_value, int):
            return current_value
        elif isinstance(current_value, bool):
            return 1 if current_value else 0
        else:
            return 0

    def update_checkbox(self, player, attribute):
        current_value = player.attribute_modifiers.get(attribute)
        if isinstance(current_value, int):
            count = current_value
        elif isinstance(current_value, bool):
            count = 1 if current_value else 0
        else:
            count = 0
        self.view.update_checkbox(attribute, count, player)

    def can_afford_item(self, item_title, player):
        item = self.get_item(item_title)
        return item and 0 <= item["price"] <= player.coins

    def get_item(self, item_title):
        return self.shop_model.get_item(item_title)

    def update_checkbox_states(self, player, screen):
        for item_title, attribute in self.ITEM_TO_ATTRIBUTE_MAP.items():
            count = player.attribute_modifiers.get(attribute)
            current_count_in_view = self.view.checkbox_counts.get(attribute)

            # Update the checkbox in the view only if the count has changed
            if count != current_count_in_view:
                self.view.update_checkbox(attribute, count, player, screen)
