import pygame


class ShopController:
    def __init__(self, model, view, screen, event_dispatcher):
        self.model = model
        self.view = view
        self.screen = screen
        self.event_dispatcher = event_dispatcher

    def handle_click(self, pos, player, action):
        for index, (tile_model, tile_view, tile_controller) in enumerate(self.view.tiles):
            if tile_controller.handle_click(pos, player, tile_model.title):
                return tile_model.title, True  # Stop the loop and return
        return None, False

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
