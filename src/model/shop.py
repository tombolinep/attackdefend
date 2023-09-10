class Shop:
    def __init__(self, player, audio_manager):
        self.player = player
        self.audio_manager = audio_manager
        self.shop_items = [
            {"title": "Quantum Thrusters", "description": "Upgrade your ship's engines for a speed boost", "price": 5,
             "limit": 5},
            {"title": "Energy Shield", "description": "Deploy an energy shield that protects against one enemy attack",
             "price": 5, "limit": 4},
            {"title": "Rapid Charge System", "description": "Enhance your ship's reload speed for the basic cannon",
             "price": 7, "limit": 3},
            {"title": "Dimensional Compression", "description": "Shrink your ship's size to avoid incoming threats",
             "price": 7, "limit": 5},
            {"title": "Tractor Beam", "description": "Install a tractor beam to collect coins from a distance",
             "price": 15, "limit": 1},
            {"title": "Warp Field Generator",
             "description": "Create a temporal field that slows enemies within its radius", "price": 20, "limit": 1},
            {"title": "Extra Blaster Mount", "description": "Mount an additional cannon for simultaneous fire",
             "price": 20, "limit": 4},
            {"title": "Rocket Launcher", "description": "Equip your ship with rocket launchers for explosive attacks",
             "price": 20, "limit": 1},
            {"title": "Laser Core Upgrade", "description": "Upgrade your ship's main cannon to a powerful laser beam",
             "price": 30, "limit": 1},
        ]

    def get_item(self, item_title):
        for item in self.shop_items:
            if item["title"] == item_title:
                return item
        return None

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

    def sell_item(self, item_title, player):
        item = self.get_item(item_title)
        if item:
            player.coins += item["price"] // 2  # You can set your own logic for selling price
            return True
        return False

    def handle_purchase(self, powerup_type, player):
        return self.buy_item(powerup_type, player)
