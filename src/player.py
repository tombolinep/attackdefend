import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH, MAIN_GAME_WIDTH


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        # Define the circle's diameter and color
        self.diameter = 50
        self.color = (0, 0, 255)  # Blue

        # Create a surface with the size of the circle's diameter
        self.surf = pygame.Surface((self.diameter, self.diameter), pygame.SRCALPHA)  # SRCALPHA for transparency

        # Draw a blue circle on the surface
        pygame.draw.circle(self.surf, self.color, (self.diameter // 2, self.diameter // 2), self.diameter // 2)

        # Get the rectangle of the surface for positioning and set its center to the screen's midpoint
        self.rect = self.surf.get_rect(center=(STATS_WIDTH + MAIN_GAME_WIDTH // 2, SCREEN_HEIGHT // 2))

        # Initialize speed attribute
        self.speed = 7

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]:
            self.move_up()
        if pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
            self.move_down()
        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
            self.move_left()
        if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
            self.move_right()

        # Keep player on the screen
        self.rect.left = max(self.rect.left, STATS_WIDTH)  # Prevent moving left of the stats screen
        self.rect.right = min(self.rect.right, SCREEN_WIDTH)  # Prevent moving right of the screen
        self.rect.top = max(self.rect.top, 0)  # Prevent moving above the screen top
        self.rect.bottom = min(self.rect.bottom, SCREEN_HEIGHT)  # Prevent moving below the screen bottom

    def move_up(self):
        self.rect.move_ip(0, -self.speed)

    def move_down(self):
        self.rect.move_ip(0, self.speed)

    def move_left(self):
        self.rect.move_ip(-self.speed, 0)

    def move_right(self):
        self.rect.move_ip(self.speed, 0)

    def speed_up(self):
        self.speed += 1  # Increase player speed by 1

    def activate_powerup(self, powerup):
        powerup.apply_powerup(self.enemies)
