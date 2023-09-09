import pygame


class ShopController:
    ACTION_BUY = "buy"
    ACTION_SELL = "sell"

    def __init__(self, model, view, screen, event_dispatcher):
        self.model = model
        self.view = view
        self.screen = screen
        self.event_dispatcher = event_dispatcher

    def handle_click(self, pos, player, item_title, action):
        for index, (tile_model, tile_view, tile_controller) in enumerate(self.view.tiles):
            if tile_model.title == item_title:  # Find the correct tile based on the title
                if tile_controller.handle_click(pos, player, tile_model.title, action):
                    return tile_model.title, True
        return None, False

    def open_shop(self, player):
        shop_running = True
        while shop_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    shop_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_button_down(event, player)

            self.view.draw(self.screen, player)
            pygame.display.flip()

    def handle_mouse_button_down(self, event, player):
        pos = event.pos

        # Check if the close button was clicked
        if self.view.close_button.is_hovered(pos):
            pygame.event.post(pygame.event.Event(pygame.QUIT))  # Dispatch a QUIT event to close the shop
            return

        action_item_tuple = self.determine_action(pos)

        # Check if action_item_tuple is None to prevent unpacking error
        if action_item_tuple is None:
            return

        action, item_title = action_item_tuple

        if action and item_title:  # Ensure both action and item_title are not None before proceeding
            self.handle_click(pos, player, item_title, action)

    def determine_action(self, pos):
        for tile_model, tile_view, tile_controller in self.view.tiles:
            if tile_view.buy_button.collidepoint(pos):
                # Handle buy button click for the current tile
                return "buy", tile_model.title
            elif tile_view.sell_button.collidepoint(pos):
                # Handle sell button click for the current tile
                return "sell", tile_model.title
        return None
