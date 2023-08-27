import pygame


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Coin, self).__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((255, 215, 0))  # Gold color for the coin
        self.draw_diamond()  # Draw the diamond shape on the coin
        self.rect = self.surf.get_rect(center=(x, y))

    def draw_diamond(self):
        # Draw a small diamond shape for the coin
        pygame.draw.polygon(self.surf, (255, 215, 0), [(10, 0), (20, 10), (10, 20), (0, 10)])
