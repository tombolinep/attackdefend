import pygame


class PowerUpController:
    def __init__(self, model):
        self.model = model

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.model.last_color_change_time >= self.model.color_change_interval:
            self.model.last_color_change_time = current_time
            self.model.current_color_index = (self.model.current_color_index + 1) % len(self.model.colors)
