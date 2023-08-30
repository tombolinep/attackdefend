import pygame


class PowerUp:
    def __init__(self):
        self.current_color_index = 0
        self.color_change_interval = 300
        self.last_color_change_time = pygame.time.get_ticks()

    def update_color(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_color_change_time >= self.color_change_interval:
            self.last_color_change_time = current_time
            self.current_color_index = (self.current_color_index + 1) % len(self.colors)
