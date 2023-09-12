import pygame
from pygame.time import get_ticks
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, audio_manager):
        super().__init__()
        self.audio_manager = audio_manager
        self.surf = pygame.Surface((10, 10))
        self.surf.fill((0, 255, 0))  # Giving it a green color for differentiation
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10  # Assuming laser to be faster than rocket
        self.target_x = target_x
        self.target_y = target_y
        self.calculate_trajectory()
        self.start_time = get_ticks()
        self.duration = 500  # Duration for which the laser exists

    def calculate_trajectory(self):
        dx = self.target_x - self.rect.x
        dy = self.target_y - self.rect.y
        distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)  # Ensure non-zero distance
        self.dx = dx / distance
        self.dy = dy / distance

    def update(self):
        current_time = get_ticks()

        if current_time - self.start_time < self.duration:
            self.rect.x += self.dx * self.speed
            self.rect.y += self.dy * self.speed
            if self.is_out_of_bounds():
                self.kill()
        else:
            self.kill()  # The laser beam will be destroyed after its duration ends

    def draw(self, screen):
        screen.blit(self.surf, self.rect)

    def is_out_of_bounds(self):
        return (self.rect.x < STATS_WIDTH or self.rect.y < 0 or
                self.rect.x > SCREEN_WIDTH or self.rect.y > SCREEN_HEIGHT)
