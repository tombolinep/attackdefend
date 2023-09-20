import pygame
from pygame.time import get_ticks
import math

from controller.laser_controller import LaserController
from view.laser_view import LaserView


class Laser(pygame.sprite.Sprite):
    def __init__(self, player, target, audio_manager, image_manager):
        super().__init__()
        self.player = player
        self.target = target
        self.audio_manager = audio_manager

        self.image = image_manager.get_image('laser')  # replace with your laser image key
        self.surf = pygame.Surface((100, 200), pygame.SRCALPHA)  # Adjust dimensions as necessary
        self.rect = self.surf.get_rect()
        self.mask = pygame.mask.from_surface(self.surf)

        self.start_point = (self.player.x, self.player.y)
        self.end_point = (self.target.x, self.target.y)
        self.speed = 5000
        self.calculate_trajectory()

        self.start_time = get_ticks()
        self.duration = 75
        self.is_shooting = True
        self.screen = pygame.display.get_surface()

        self.view = LaserView(self)
        self.controller = LaserController(self, self.view)

    def calculate_trajectory(self):
        self.dx = self.target.x - self.start_point[0]
        self.dy = self.target.y - self.start_point[1]

        self.angle = math.degrees(math.atan2(self.dy, self.dx)) - 90
        self.length = math.hypot(self.dx, self.dy)  # Calculate the full length

    def update(self):
        self.controller.update()
