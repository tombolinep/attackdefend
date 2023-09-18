from math import log

import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH, JUNK_WIDTH, JUNK_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT

ENEMY_IMAGES = [
    pygame.image.load('assets/junk1.png'),
    pygame.image.load('assets/junk2.png'),
    pygame.image.load('assets/junk3.png'),
]

ENEMY_RED_IMAGE = pygame.image.load('assets/enemy_red.png')

ENEMY_ROTATIONS = []
for image in ENEMY_IMAGES:
    ENEMY_ROTATIONS.extend([pygame.transform.rotate(image, i) for i in random.sample(range(0, 360), 5)])


class Enemy(pygame.sprite.Sprite):
    def __init__(self, score, player, enemy_type="white"):
        super().__init__()
        self.player = player
        self.type = enemy_type
        if self.type == "red":
            self.image = ENEMY_RED_IMAGE
            self.surf = pygame.transform.scale(self.image, (ENEMY_WIDTH, ENEMY_HEIGHT))

        else:
            self.image = random.choice(ENEMY_ROTATIONS)
            self.surf = pygame.transform.scale(self.image, (JUNK_WIDTH, JUNK_HEIGHT))

        self.rect = self.surf.get_rect()
        self.mask = pygame.mask.from_surface(self.surf)
        self.radius = self.rect.width / 2

        max_speed = 12
        min_speed = 1
        speed_range = max_speed - min_speed

        self.base_speed = random.uniform(0.1, 0.5)
        self.adjusted_speed = self.base_speed + log(max(1, score + 1)) * 0.15  # Slow increment based on score
        self.speed = max(1, min(self.adjusted_speed, 12))

        self.previous_speed = None
        self.initial_position()
        self.in_warp_field = False

    def initial_position(self):
        side = random.randint(0, 3)
        if side == 0:  # top
            self.rect = self.surf.get_rect(center=(random.randint(STATS_WIDTH, SCREEN_WIDTH), -10))
            self.dx, self.dy = 0, self.speed
        elif side == 1:  # right
            self.rect = self.surf.get_rect(center=(SCREEN_WIDTH + 10, random.randint(0, SCREEN_HEIGHT)))
            self.dx, self.dy = -self.speed, 0
        elif side == 2:  # bottom
            self.rect = self.surf.get_rect(center=(random.randint(STATS_WIDTH, SCREEN_WIDTH), SCREEN_HEIGHT + 10))
            self.dx, self.dy = 0, -self.speed
        else:  # left
            self.rect = self.surf.get_rect(center=(STATS_WIDTH - 10, random.randint(0, SCREEN_HEIGHT)))
            self.dx, self.dy = self.speed, 0

    def update_position(self):
        slowdown_factor = 0.8 if self.in_warp_field else 1.0

        if self.type == "red":
            dx, dy = self.get_direction_towards_player()
            self.move(dx, dy, slowdown_factor)
        else:
            self.rect.move_ip(round(self.dx * slowdown_factor), round(self.dy * slowdown_factor))

        if (self.rect.right < STATS_WIDTH or self.rect.left > SCREEN_WIDTH or
                self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.kill()

    def get_direction_towards_player(self):
        player_center = self.player.rect.center
        dx = player_center[0] - self.rect.centerx
        dy = player_center[1] - self.rect.centery

        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance > 0:
            dx /= distance
            dy /= distance

        return dx, dy

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
