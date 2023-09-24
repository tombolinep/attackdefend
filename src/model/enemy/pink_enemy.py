import pygame
import time

from constants import ENEMY_WIDTH, ENEMY_HEIGHT
from model.enemy.enemy import EnemyBase


class PinkEnemy(EnemyBase):
    def __init__(self, score, player, image_manager, settings):
        super().__init__(score, player, image_manager, settings)
        self.type = "pink"
        self.zigzag = True  # To decide zigzag direction
        self.last_sprint_time = time.time()
        self.sprint_duration = 1  # Sprint for 2 seconds
        self.sprint_interval = 4  # 5 seconds between each sprint
        self.sprint_speed_factor = 1.5  # Speed multiplier during sprint
        self.zigzag_factor = 5  # Bigger values will result in more pronounced zigzagging

    def set_image(self, image_manager):
        raw_surf = image_manager.get_image('enemy_pink')
        self.surf = pygame.transform.scale(raw_surf, (ENEMY_WIDTH, ENEMY_HEIGHT))
        self.rect = self.surf.get_rect()
        self.mask = pygame.mask.from_surface(self.surf)
        self.radius = self.rect.width / 2

    def update_position(self):
        current_time = time.time()
        dx, dy = self.get_direction_towards_player()

        # Sprinting logic
        if current_time - self.last_sprint_time > self.sprint_interval + self.sprint_duration:
            self.last_sprint_time = current_time

        is_sprinting = current_time - self.last_sprint_time < self.sprint_duration
        speed_factor = self.sprint_speed_factor if is_sprinting else 1.0

        # Zigzag logic
        zigzag_modifier = self.zigzag_factor if self.zigzag else -self.zigzag_factor
        self.zigzag = not self.zigzag  # Toggle direction for next update

        # Apply zigzag only when not sprinting
        if not is_sprinting:
            dx += zigzag_modifier
            dy += zigzag_modifier  # optionally apply to dy as well

        slowdown_factor = 0.8 if self.in_warp_field else 1.0
        self.move(dx * speed_factor, dy * speed_factor, slowdown_factor)

        if self.rect.right < self.settings.STATS_WIDTH:
            self.kill()
