import pygame


class ShopController:
    def __init__(self, model, view, screen, event_dispatcher):
        self.model = model
        self.view = view
        self.screen = screen
        self.event_dispatcher = event_dispatcher

    def handle_click(self, pos, player, action="buy"):
        x, y = pos
        for index, item in enumerate(self.model.shop_items):
            tile_x = self.view.x + (index % 3) * self.view.tile_width
            tile_y = self.view.y + (index // 3) * self.view.tile_height

            if tile_x <= x <= tile_x + self.view.tile_width and tile_y <= y <= tile_y + self.view.tile_height:
                message_position = (tile_x + 10, tile_y + 10)  # Position for the message

                success = False  # Initialize a success flag
                if action == "buy":
                    if self.model.can_afford_item(item["title"], player):
                        success = self.model.buy_item(item["title"], player)
                        self.event_dispatcher.dispatch_event("buy_item", {"title": item["title"], "success": success})

                elif action == "sell":
                    success = self.model.sell_item(item["title"], player)
                    self.event_dispatcher.dispatch_event("sell_item", {"title": item["title"], "success": success})

                # Display purchase message based on success
                if success:
                    self.view.display_purchase_message(self.screen, message_position, "Bought!", (0, 255, 0))
                else:
                    self.view.display_purchase_message(self.screen, message_position, "Error", (255, 0, 0))

                return item["title"], success  # Stop the loop and return

        return None, False  # If no item was clicked

    def open_shop(self, player):
        shop_running = True
        while shop_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    shop_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    action = "buy"  # Set some condition to determine buy or sell action
                    self.handle_click(pos, player, action)

            self.view.draw(self.screen, player)
            pygame.display.flip()
