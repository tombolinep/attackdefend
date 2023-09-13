import pygame


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((255, 175, 0))
        self.x = x
        self.y = y

        self.colors = [
            (255, 175, 0),
            (255, 200, 0),
            (255, 222, 0),
            (255, 255, 0)
        ]

        self.current_color_index = 0
        self.color_change_interval = 500
        self.last_color_change_time = pygame.time.get_ticks()

        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_color_change_time >= self.color_change_interval:
            self.last_color_change_time = current_time
            self.current_color_index = (self.current_color_index + 1) % len(self.colors)
            self.surf.fill(self.colors[self.current_color_index])  # Update color
        self.rect.x = self.x
        self.rect.y = self.y