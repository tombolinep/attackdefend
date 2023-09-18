import pygame
from pygame.time import get_ticks
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH, LASER_COLOUR, MAIN_GAME_WIDTH


class Laser(pygame.sprite.Sprite):
    def __init__(self, player, target, audio_manager, image_manager):
        super().__init__()
        self.player = player
        self.target = target
        self.audio_manager = audio_manager

        self.start_point = (self.player.x, self.player.y)  #
        self.end_point = (self.player.x, self.player.y)

        self.speed = 5000

        self.calculate_trajectory()

        self.start_time = get_ticks()
        self.duration = 75

        self.is_shooting = True
        self.screen = pygame.display.get_surface()

        self.surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.rect = self.surf.get_rect()

    def calculate_trajectory(self):
        # Set the trajectory to directly hit the target point
        self.dx = self.target.x - self.start_point[0]
        self.dy = self.target.y - self.start_point[1]

    def shoot(self):
        self.surf.fill((0, 0, 0, 0))  # Clearing the surface at the start of each shoot call

        # Update the target position to point to the center of the enemy rect
        target_center_x = self.target.x + self.target.width / 2
        target_center_y = self.target.y + self.target.height / 2

        self.start_point = (self.player.x, self.player.y)  # Update the start point to the player's current position

        # Set the end point to the target's center coordinates
        self.end_point = (target_center_x, target_center_y)

        laser_radius = 5  # Adjust the radius as necessary

        # Draw the laser on the surface
        pygame.draw.line(self.surf, LASER_COLOUR, self.start_point, self.end_point, laser_radius * 2)
        pygame.draw.circle(self.surf, LASER_COLOUR, self.start_point, laser_radius)
        pygame.draw.circle(self.surf, LASER_COLOUR, (int(self.end_point[0]), int(self.end_point[1])), laser_radius)

    def update(self):
        self.start_point = (self.player.x, self.player.y)

        current_time = get_ticks()
        if self.is_shooting:
            if current_time - self.start_time < self.duration:
                self.shoot()
            else:
                self.is_shooting = False
                self.kill()
