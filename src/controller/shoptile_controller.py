from controller.shop_controller import ShopController


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

    ATTRIBUTE_CHANGE_AMOUNTS = {
        "Quantum Thrusters": 1,
        "Energy Shield": 1,
        "Rapid Charge System": 1,
        "Dimensional Compression": 1,
        "Tractor Beam": True,
        "Warp Field Generator": True,
        "Extra Blaster Mount": True,
        "Rocket Launcher": True,
        "Laser Core Upgrade": True,
    }

    CUSTOM_MODIFIERS = {
        "Dimensional Compression": -5,
        "Rapid Charge System": -0.5,
    }

    def __init__(self, model, view, event_dispatcher, shop_model, audio_manager):
        self.model = model
        self.view = view
        self.event_dispatcher = event_dispatcher
        self.shop_model = shop_model
        self.audio_manager = audio_manager

    def handle_click(self, player, item_title, action):
        item_price = self.get_item_price(item_title)
        attribute_to_update = self.get_attribute_to_update(item_title)
        if action == ShopController.ACTION_BUY:
            return self.handle_buy(player, item_title, item_price, attribute_to_update)
        elif action == ShopController.ACTION_SELL:
            return self.handle_sell(player, item_price, attribute_to_update)

    def update_player_attribute(self, player, attribute_to_update, increment=True):
        base_value = player.ATTRIBUTE_DEFAULTS.get(attribute_to_update)
        modifier = player.attributes_bought.get(attribute_to_update, 0)

        item_title = self.get_item_title_from_attribute(attribute_to_update)
        change_amount = self.ATTRIBUTE_CHANGE_AMOUNTS.get(item_title)
        custom_modifier = self.CUSTOM_MODIFIERS.get(item_title, 1)

        if increment:
            modifier += change_amount
        else:
            modifier -= change_amount

        new_value = base_value + (modifier * custom_modifier)

        setattr(player, attribute_to_update, new_value)
        player.attributes_bought[attribute_to_update] = modifier

    def handle_buy(self, player, item_title, item_price, attribute_to_update):
        item_limit = self.model.limit
        current_quantity = player.attributes_bought.get(attribute_to_update, 0)

        change_amount = self.ATTRIBUTE_CHANGE_AMOUNTS.get(item_title)

        if item_limit is not None and current_quantity >= item_limit * change_amount:
            self.view.set_status_message("Item limit reached", (255, 0, 0), "buy")
            self.audio_manager.play_purchase_error_sound()
            return False

        if self.can_afford_item(item_title, player):
            player.add_coin(-item_price)
            self.update_player_attribute(player, attribute_to_update, increment=True)
            self.view.set_status_message("Bought!", (0, 255, 0), "buy")
            self.audio_manager.play_purchase_success_sound()
            return True
        else:
            self.view.set_status_message("Cannot afford", (255, 0, 0), "buy")
            self.audio_manager.play_purchase_error_sound()
            return False

    def handle_sell(self, player, item_price, attribute_to_update):

        if player.can_sell_item(attribute_to_update, 1):
            player.add_coin(int(item_price * 0.7))
            self.update_player_attribute(player, attribute_to_update, increment=False)
            self.view.set_status_message("Sold!", (0, 255, 0), "sell")
            self.audio_manager.play_purchase_success_sound()
            return True
        else:
            self.view.set_status_message("Cannot sell", (255, 0, 0), "sell")
            self.audio_manager.play_purchase_error_sound()
            return False

    def get_item_title_from_attribute(self, attribute):
        for item_title, item_attribute in self.ITEM_TO_ATTRIBUTE_MAP.items():
            if item_attribute == attribute:
                return item_title

    def get_item_price(self, item_title):
        return self.get_item(item_title).get('price', 0)

    def get_attribute_to_update(self, item_title):
        return self.ITEM_TO_ATTRIBUTE_MAP.get(item_title, None)

    def can_afford_item(self, item_title, player):
        item = self.get_item(item_title)
        return item and 0 <= item["price"] <= player.coins

    def get_item(self, item_title):
        return self.shop_model.get_item(item_title)
