import pygame
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH, MAIN_GAME_WIDTH


class Player(pygame.sprite.Sprite):
    SHIELD_COLORS = [(205, 127, 50), (192, 192, 192), (255, 223, 0), (0, 255, 255)]  # Bronze, Silver, Gold, Platinum

    def __init__(self):
        super(Player, self).__init__()
        self._initialize_graphics()
        self.speed = 7
        self.coins = 20
        self.shield = 0

    def _initialize_graphics(self):
        self.diameter = 50
        self.shield_ring_radius = self.diameter // 2 + len(Player.SHIELD_COLORS) * 5
        self.color = (0, 0, 255)  # Blue

        # Create a larger surface to accommodate the shield rings
        self.surf = pygame.Surface((self.shield_ring_radius * 2, self.shield_ring_radius * 2), pygame.SRCALPHA)

        pygame.draw.circle(self.surf, self.color, (self.shield_ring_radius, self.shield_ring_radius),
                           self.diameter // 2)
        self.rect = self.surf.get_rect(center=(STATS_WIDTH + MAIN_GAME_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.shield_surf = pygame.Surface((self.shield_ring_radius * 2, self.shield_ring_radius * 2),
                                          pygame.SRCALPHA)  # Surface for shield rings

    def update(self, pressed_keys):
        self._handle_movement(pressed_keys)
        self._keep_within_boundaries()

    def _handle_movement(self, pressed_keys):
        if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]: self.move_up()
        if pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]: self.move_down()
        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]: self.move_left()
        if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]: self.move_right()

    def _keep_within_boundaries(self):
        self.rect.left = max(self.rect.left, STATS_WIDTH)
        self.rect.right = min(self.rect.right, SCREEN_WIDTH)
        self.rect.top = max(self.rect.top, 0)
        self.rect.bottom = min(self.rect.bottom, SCREEN_HEIGHT)

    def move_up(self):
        self.rect.move_ip(0, -self.speed)

    def move_down(self):
        self.rect.move_ip(0, self.speed)

    def move_left(self):
        self.rect.move_ip(-self.speed, 0)

    def move_right(self):
        self.rect.move_ip(self.speed, 0)

    def add_coin(self):
        self.coins += 1

    def deduct_coin(self, amount):
        if self.coins >= amount:
            self.coins -= amount
            return True
        return False

    def increase_speed(self, increment=2):  # Increment can be adjusted based on your game's needs
        self.speed += increment

    def add_shield(self):
        self.shield += 1
        self._draw_shield_rings()

    def remove_shield(self):
        if self.shield > 0:
            self.shield -= 1
            self._draw_shield_rings()

            # Ensure the updated shield rings are on the main surface (self.surf)
            self.surf.fill((0, 0, 0, 0))
            pygame.draw.circle(self.surf, self.color, (self.shield_ring_radius, self.shield_ring_radius),
                               self.diameter // 2)
            self.surf.blit(self.shield_surf, (0, 0))

    def get_shield(self):
        return self.shield

    def purchase_item(self, price):
        if self.coins >= price:
            self.coins -= price
            return True
        return False

    def _draw_shield_rings(self):
        self.shield_surf.fill((0, 0, 0, 0))  # Clear the shield surface
        for level in range(self.shield):
            ring_color = Player.SHIELD_COLORS[level % len(Player.SHIELD_COLORS)]
            ring_center = (self.shield_ring_radius, self.shield_ring_radius)
            ring_radius = self.diameter // 2 + (level + 1) * 5  # Increase the radius for each ring
            pygame.draw.circle(self.shield_surf, ring_color, ring_center, ring_radius, 3)
        self.surf.blit(self.shield_surf, (0, 0))

    def draw(self, screen):
        self._draw_shield_rings()  # Draw shield rings on the shield surface
        self.surf.blit(self.shield_surf, (0, 0))  # Blit the shield surface onto the main surface
        screen.blit(self.surf, self.rect)  # Draw the main surface on the screen
