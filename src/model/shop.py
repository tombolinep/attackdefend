class Shop:
    def __init__(self):
        self.shop_items = [
            {"title": "Speed Boost", "description": "Increases player speed", "price": 5},
            {"title": "Shield", "description": "Protects from one enemy", "price": 5},
            {"title": "tbd", "description": "coming soon", "price": -1},
            {"title": "tbd", "description": "coming soon", "price": -1},
            {"title": "tbd", "description": "coming soon", "price": -1},
            {"title": "tbd", "description": "coming soon", "price": -1},
            {"title": "tbd", "description": "coming soon", "price": -1},
            {"title": "tbd", "description": "coming soon", "price": -1},
            {"title": "tbd", "description": "coming soon", "price": -1},
        ]

    def get_item(self, item_title):
        for item in self.shop_items:
            if item["title"] == item_title:
                return item
        return None

    def can_afford_item(self, item_title, player):
        item = self.get_item(item_title)
        return item and 0 <= item["price"] <= player.coins

    def buy_item(self, item_title, player):
        item = self.get_item(item_title)
        if item and item["price"] <= player.coins:
            if item["title"] == "Speed Boost":
                player.increase_speed()
            elif item["title"] == "Shield":
                if player.get_shield() <= 3:
                    player.add_shield()
                else:
                    return False
            player.coins -= item["price"]
            return True
        return False

    def handle_purchase(self, powerup_type, player):
        return self.buy_item(powerup_type, player)
