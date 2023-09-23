import pygame
import math
from pygame.time import get_ticks
from controller.rocket_controller import RocketController
from view.rocket_view import RocketView


class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, audio_manager, image_manager, settings):
        super().__init__()
        self.settings = settings
        self.audio_manager = audio_manager
        self.image_manager = image_manager
        self.rocket_image = self.image_manager.get_image('rocket')
        self.explosion_image = self.image_manager.get_image('explosion')
        self.image = self.rocket_image
        self.surf = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.surf.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.surf)
        self.speed = 5
        self.target_x = target_x
        self.target_y = target_y
        self.calculate_trajectory()
        self.start_time = get_ticks()
        self.explosion_time = 1350
        self.explosion_radius = 150
        self.is_exploding = False
        self.explosion_duration = 1000
        self.screen = pygame.display.get_surface()
        self.view = RocketView(self)
        self.controller = RocketController(self, self.view, self.settings)
        self.just_exploded = False  # The flag for the initial explosion frame
        self.angle_index = 0
        self.angle = 0  # Initialize angle to zero
        self.calculate_trajectory()
        self.update_image_rotation()

    def calculate_trajectory(self):
        dx = self.target_x - self.rect.x
        dy = self.target_y - self.rect.y
        distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)
        self.dx = dx / distance
        self.dy = dy / distance

        # Calculate the angle based on the direction of movement
        # Negative sign for 'dy' to account for the inverted y-axis in Pygame
        self.angle = math.degrees(math.atan2(-dy, dx))

        # Adding 90 degrees to align with the rocket's default orientation
        self.angle = (self.angle + 90) % 360
        self.update_image_rotation()

    def update_image_rotation(self):
        # Find the closest cached angle to self.angle
        closest_angle = round(self.angle / 15) * 15
        closest_angle %= 360  # Ensure it's within [0, 360)

        # Adjusting for the mirrored look
        corrected_angle = 360 - closest_angle

        # Flip it by 180 degrees to have the nose point forward
        corrected_angle = (corrected_angle + 180) % 360

        self.image = self.image_manager.rotated_rockets[corrected_angle]
        self.surf = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.surf.get_rect(center=self.rect.center)

    def explode(self):
        self.is_exploding = True
        self.just_exploded = True
        self.start_time = get_ticks()
        self.audio_manager.play_rocket_explosion()

        # Initial size setup for the explosion
        initial_size = int(0.5 * self.explosion_radius * 2)
        self.image = pygame.transform.scale(self.explosion_image, (initial_size, initial_size))
        self.surf = self.image
        self.rect = self.surf.get_rect(center=self.rect.center)

    def update(self):
        self.controller.update()
