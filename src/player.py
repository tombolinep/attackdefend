import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        # Define the circle's diameter and color
        self.diameter = 75
        self.color = (0, 0, 255)  # Blue

        # Create a surface with the size of the circle's diameter
        self.surf = pygame.Surface((self.diameter, self.diameter), pygame.SRCALPHA)  # SRCALPHA for transparency

        # Draw a blue circle on the surface
        pygame.draw.circle(self.surf, self.color, (self.diameter // 2, self.diameter // 2), self.diameter // 2)

        # Get the rectangle of the surface for positioning and set its center to the screen's midpoint
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_UP]:
            self.rect.move_ip(0, -15)
        if pressed_keys[pygame.K_DOWN]:
            self.rect.move_ip(0, 15)
        if pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-15, 0)
        if pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(15, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
