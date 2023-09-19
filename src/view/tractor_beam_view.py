import pygame
import math


class TractorBeamView:
    def __init__(self, model):
        self.model = model

    def draw(self, screen, player_position, coin_position):
        # Calculate the angle to rotate the image
        dx = coin_position[0] - player_position[0]
        dy = coin_position[1] - player_position[1]
        angle = math.degrees(math.atan2(dy, dx)) - 90

        # Calculate the length of the beam based on the distance to the coin and add a fixed value
        beam_length = min(100, math.hypot(dx, dy)) + 100  # Adjust the fixed value as needed

        # Rotate and scale the image
        rotated_image = pygame.transform.rotate(
            pygame.transform.scale(self.model.image, (100, int(beam_length))), -angle)

        # Create a new surf with dimensions matching the rotated image
        self.model.surf = pygame.Surface((rotated_image.get_width(), rotated_image.get_height()), pygame.SRCALPHA)

        # Calculate the adjusted player position
        adjusted_player_position = (player_position[0] + math.cos(math.radians(angle + 90)) * (beam_length / 2),
                                    player_position[1] + math.sin(math.radians(angle + 90)) * (beam_length / 2))

        # Get the new rect of the rotated image and set its center to the adjusted player's center
        self.model.rect = rotated_image.get_rect(center=adjusted_player_position)

        # Blit the rotated image onto the new surf
        self.model.surf.blit(rotated_image, (0, self.model.surf.get_height() - rotated_image.get_height()))

        # Draw the surf onto the screen
        screen.blit(self.model.surf, self.model.rect.topleft)
