import pygame


class Coin:
    def __init__(self, x, y):
        self.colors = [
            (255, 175, 0),
            (255, 200, 0),
            (255, 222, 0),
            (255, 255, 0)
        ]
        self.current_color_index = 0
        self.color_change_interval = 500
        self.last_color_change_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(x, y, 20, 20)
