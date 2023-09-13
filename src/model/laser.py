import pygame
from pygame.time import get_ticks
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH, LASER_COLOUR, MAIN_GAME_WIDTH


class Laser(pygame.sprite.Sprite):
    def __init__(self, player, target_x, target_y, audio_manager):
        super().__init__()
        self.player = player
        self.audio_manager = audio_manager

        self.start_point = (self.player.x, self.player.y)  #
        self.end_point = (self.player.x, self.player.y)

        self.target_x = target_x
        self.target_y = target_y
        self.speed = 50

        self.calculate_trajectory()

        self.start_time = get_ticks()
        self.duration = 75

        self.is_shooting = True
        self.screen = pygame.display.get_surface()

        self.surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.rect = self.surf.get_rect()

    def calculate_trajectory(self):
        # Set the trajectory to directly hit the target point
        self.dx = self.target_x - self.start_point[0]
        self.dy = self.target_y - self.start_point[1]

    def shoot(self):
        self.surf.fill((0, 0, 0, 0))  # Clearing the surface at the start of each shoot call

        self.start_point = (self.player.x, self.player.y)  # Update the start point to the player's current position

        # Set the end point directly to the target coordinates
        self.end_point = (self.target_x, self.target_y)

        laser_radius = 5  # Adjust the radius as necessary

        # Create a temporary surface to find the bounding rect
        temp_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        # Draw the laser on the temporary surface
        pygame.draw.line(temp_surf, LASER_COLOUR, self.start_point, self.end_point, laser_radius * 2)
        pygame.draw.circle(temp_surf, LASER_COLOUR, self.start_point, laser_radius)
        pygame.draw.circle(temp_surf, LASER_COLOUR, (int(self.end_point[0]), int(self.end_point[1])), laser_radius)

        # Get the bounding rect of the laser on the temporary surface
        self.rect = temp_surf.get_bounding_rect()

        # Create a new surface with dimensions of the bounding rect
        self.surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)

        # Calculate the start and end points relative to the new surface
        start_point_rel = (self.start_point[0] - self.rect.x, self.start_point[1] - self.rect.y)
        end_point_rel = (self.end_point[0] - self.rect.x, self.end_point[1] - self.rect.y)

        # Draw the laser on the new surface using the relative start and end points
        pygame.draw.line(self.surf, LASER_COLOUR, start_point_rel, end_point_rel, laser_radius * 2)
        pygame.draw.circle(self.surf, LASER_COLOUR, start_point_rel, laser_radius)
        pygame.draw.circle(self.surf, LASER_COLOUR, end_point_rel, laser_radius)

    def draw(self, screen):
        # Blit the surface onto the screen using the laser's rect
        screen.blit(self.surf, self.rect.topleft)

    def update(self):
        self.start_point = (self.player.x, self.player.y)

        current_time = get_ticks()
        if self.is_shooting:
            if current_time - self.start_time < self.duration:
                self.shoot()
            else:
                self.is_shooting = False
                self.kill()

    def get_mask(self):
        return pygame.mask.from_surface(self.surf)
