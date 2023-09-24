from math import log
import pygame
import random

class EnemyBase(pygame.sprite.Sprite):
    def __init__(self, score, player, image_manager, settings):
        super().__init__()
        self.settings = settings
        self.player = player
        self.rect = None
        self.surf = None
        self.mask = None
        self.radius = None

        self.in_warp_field = False
        self.base_speed = random.uniform(0.1, 0.5)
        self.adjusted_speed = self.base_speed + log(max(1, score + 1)) * 0.15
        self.speed = max(1, min(self.adjusted_speed, 12))

        self.set_image(image_manager)
        self.initial_position()  # Now `self.speed` is already initialized

    def set_image(self, image_manager):
        pass  # Implement in subclasses

    def initial_position(self):
        side = random.randint(0, 3)
        if side == 0:  # top
            self.rect = self.surf.get_rect(
                center=(random.randint(self.settings.STATS_WIDTH, self.settings.SCREEN_WIDTH), -10))
            self.dx, self.dy = 0, self.speed
        elif side == 1:  # right
            self.rect = self.surf.get_rect(
                center=(self.settings.SCREEN_WIDTH + 10, random.randint(0, self.settings.SCREEN_HEIGHT)))
            self.dx, self.dy = -self.speed, 0
        elif side == 2:  # bottom
            self.rect = self.surf.get_rect(center=(
                random.randint(self.settings.STATS_WIDTH, self.settings.SCREEN_WIDTH),
                self.settings.SCREEN_HEIGHT + 10))
            self.dx, self.dy = 0, -self.speed
        else:  # left
            self.rect = self.surf.get_rect(
                center=(self.settings.STATS_WIDTH - 10, random.randint(0, self.settings.SCREEN_HEIGHT)))
            self.dx, self.dy = self.speed, 0

    def update_position(self):
        slowdown_factor = 0.8 if self.in_warp_field else 1.0
        self.rect.move_ip(round(self.dx * slowdown_factor), round(self.dy * slowdown_factor))
        if self.rect.right < self.settings.STATS_WIDTH:
            self.kill()

    def move(self, dx, dy, slowdown_factor):
        new_speed = max(1, self.speed * slowdown_factor)  # Ensure minimum speed of 1

        new_x = self.rect.x + round(dx * new_speed)
        new_y = self.rect.y + round(dy * new_speed)

        player_center = self.player.rect.center

        proposed_dist_to_player = ((player_center[0] - new_x) ** 2 + (player_center[1] - new_y) ** 2) ** 0.5

        if proposed_dist_to_player < (
                (player_center[0] - self.rect.x) ** 2 + (player_center[1] - self.rect.y) ** 2) ** 0.5:
            self.rect.x = new_x
            self.rect.y = new_y

    def get_direction_towards_player(self):
        player_center = self.player.rect.center
        dx = player_center[0] - self.rect.centerx
        dy = player_center[1] - self.rect.centery

        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance > 0:
            dx /= distance
            dy /= distance

        return dx, dy