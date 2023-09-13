import pygame
from pygame.time import get_ticks
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, audio_manager):
        super().__init__()
        self.audio_manager = audio_manager

        self.start_point = (x, y)
        self.end_point = (x, y)  # Initially, the end point is the start point

        self.target_x = target_x
        self.target_y = target_y
        self.speed = 5  # Adjust speed as necessary

        self.calculate_trajectory()

        self.start_time = get_ticks()
        self.duration = 1500  # Adjust duration as necessary

        self.is_shooting = True
        self.screen = pygame.display.get_surface()  # Get the currently set video surface

        self.surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)  # Creating a transparent surface
        self.rect = self.surf.get_rect()

    def calculate_trajectory(self):
        dx = self.target_x - self.start_point[0]
        dy = self.target_y - self.start_point[1]
        distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)  # Ensure non-zero distance
        self.dx = dx / distance
        self.dy = dy / distance

    def shoot(self):
        self.surf.fill((0, 0, 0, 0))  # Clearing the surface at the start of each shoot call
        self.end_point = (self.end_point[0] + self.dx * self.speed, self.end_point[1] + self.dy * self.speed)
        pygame.draw.line(self.surf, (0, 255, 0), self.start_point, self.end_point, 2)

    def draw(self, screen):
        # Blit the surface onto the screen
        screen.blit(self.surf, (0, 0))

    def update(self):
        current_time = get_ticks()

        if self.is_shooting:
            if current_time - self.start_time < self.duration:
                self.shoot()
            else:
                self.is_shooting = False
                self.kill()
