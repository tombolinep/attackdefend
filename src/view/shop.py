import pygame


class ShopView:
    def __init__(self, x, y, width, height, shop_items):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.shop_items = shop_items

    def draw(self, screen, player):
        self.create_shop_window(screen)
        for index, item in enumerate(self.shop_items):
            self.create_shop_button(screen, item, index)

    def create_shop_window(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width * len(self.shop_items), self.height))

    def create_shop_button(self, screen, item, index):
        pygame.draw.rect(screen, item['color'], (self.x + index * 100, self.y, self.width, self.height))
        text = pygame.font.SysFont('Arial', 20).render(item['title'], True, (0, 0, 0))
        screen.blit(text, (self.x + index * 100 + 15, self.y + 25))
        
    def display_purchase_message(self, screen, position, message):
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 30)
        text_surface = font.render(message, True, (255, 255, 255))
        screen.blit(text_surface, position)