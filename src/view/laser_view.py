import math

import pygame
from constants import LASER_SIZE


class LaserView:
    def __init__(self, model):
        self.model = model

    def draw(self, screen):
        # Calculate the new position and dimensions of the laser
        rotated_image = pygame.transform.rotate(
            pygame.transform.scale(self.model.image, (LASER_SIZE, int(self.model.length))), -self.model.angle)

        # Create a new surface with dimensions matching the rotated image
        self.model.surf = pygame.Surface((rotated_image.get_width(), rotated_image.get_height()), pygame.SRCALPHA)

        # Find the new center of the rotated image
        adjusted_start_position = (
            self.model.start_point[0] + math.cos(math.radians(self.model.angle + 90)) * (self.model.length / 2),
            self.model.start_point[1] + math.sin(math.radians(self.model.angle + 90)) * (self.model.length / 2)
        )

        # Get the new rectangle of the rotated image and set its center to the new center
        self.model.rect = rotated_image.get_rect(center=adjusted_start_position)

        # Blit the rotated image onto the new surface
        self.model.surf.blit(rotated_image, (0, 0))

        # Draw the surface onto the screen
        screen.blit(self.model.surf, self.model.rect.topleft)
