import pygame


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Coin, self).__init__()

        self.colors = [
            (255, 175, 0),  # Deeper gold
            (255, 200, 0),  # Slightly lighter
            (255, 222, 0),  # Even lighter
            (255, 255, 0)  # Lightest shade
        ]
        self.current_color_index = 0
        self.color_change_interval = 500  # Change color every half second
        self.last_color_change_time = pygame.time.get_ticks()

        self.surf = pygame.Surface((20, 20))
        self.update_surface()  # Use this to fill the surface with the current color
        self.rect = self.surf.get_rect(center=(x, y))

    def update_surface(self):
        # Use the current color to fill the surface
        self.surf.fill(self.colors[self.current_color_index])

    def update_color(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_color_change_time >= self.color_change_interval:
            self.last_color_change_time = current_time
            self.current_color_index = (self.current_color_index + 1) % len(self.colors)
            self.update_surface()

    def update(self):
        self.update_color()
