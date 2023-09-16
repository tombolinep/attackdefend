import pygame
from pygame.time import get_ticks
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH


class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, audio_manager):
        super().__init__()
        self.audio_manager = audio_manager
        self.surf = pygame.Surface((20, 20))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.target_x = target_x
        self.target_y = target_y
        self.calculate_trajectory()
        self.start_time = get_ticks()
        self.explosion_time = 1500  # Rocket will explode after 1500 milliseconds (1.5 seconds)
        self.explosion_radius = 150  # Radius of the explosion effect
        self.is_exploding = False
        self.explosion_duration = 100

    def calculate_trajectory(self):
        dx = self.target_x - self.rect.x
        dy = self.target_y - self.rect.y
        distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)  # Ensure non-zero distance
        self.dx = dx / distance
        self.dy = dy / distance

    def update(self):
        current_time = get_ticks()

        if not self.is_exploding:
            self.rect.x += self.dx * self.speed
            self.rect.y += self.dy * self.speed

            if current_time - self.start_time >= self.explosion_time:
                self.explode()
            elif self.is_out_of_bounds():
                self.kill()
        else:
            if current_time - self.start_time - self.explosion_time >= self.explosion_duration:
                self.kill()

    def explode(self):
        self.is_exploding = True
        self.start_time = get_ticks()
        self.surf = pygame.Surface((self.explosion_radius * 2, self.explosion_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.surf, (255, 0, 0, 128), (self.explosion_radius, self.explosion_radius),
                           self.explosion_radius)
        self.audio_manager.play_rocket_explosion()
        self.rect = self.surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        if not self.is_exploding:
            screen.blit(self.surf, self.rect)
        else:
            explosion_rect = self.surf.get_rect(center=self.rect.center)
            screen.blit(self.surf, explosion_rect)

    def is_out_of_bounds(self):
        return (self.rect.x < STATS_WIDTH or self.rect.y < 0 or
                self.rect.x > SCREEN_WIDTH or self.rect.y > SCREEN_HEIGHT)