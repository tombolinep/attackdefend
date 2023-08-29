# player_view.py
import pygame
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH, MAIN_GAME_WIDTH


class PlayerView:

    def __init__(self, model):
        self.model = model
        self.SHIELD_COLORS = [(205, 127, 50), (192, 192, 192), (255, 223, 0), (0, 255, 255)]
        self._initialize_graphics()

    def _initialize_graphics(self):
        self.diameter = 50
        self.shield_ring_radius = self.diameter // 2 + len(self.SHIELD_COLORS) * 5
        self.color = (0, 0, 255)  # Blue

        # Create a larger surface to accommodate the shield rings
        self.surf = pygame.Surface((self.shield_ring_radius * 2, self.shield_ring_radius * 2), pygame.SRCALPHA)

        pygame.draw.circle(self.surf, self.color, (self.shield_ring_radius, self.shield_ring_radius),
                           self.diameter // 2)
        self.rect = self.surf.get_rect(center=(STATS_WIDTH + MAIN_GAME_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.shield_surf = pygame.Surface((self.shield_ring_radius * 2, self.shield_ring_radius * 2),
                                          pygame.SRCALPHA)  # Surface for shield rings

    def _draw_shield_rings(self):
        self.shield_surf.fill((0, 0, 0, 0))  # Clear the shield surface
        for level in range(self.shield):
            ring_color = self.SHIELD_COLORS[level % len(self.SHIELD_COLORS)]
            ring_center = (self.shield_ring_radius, self.shield_ring_radius)
            ring_radius = self.diameter // 2 + (level + 1) * 5  # Increase the radius for each ring
            pygame.draw.circle(self.shield_surf, ring_color, ring_center, ring_radius, 3)
        self.surf.blit(self.shield_surf, (0, 0))

    def draw(self, screen):
        # Use attributes from self.model to draw the player
        screen.blit(self.model.image, self.model.rect)

    def update_shield(self):
        if self.model.get_shield() > 0:
            self._draw_shield_rings()
            self.surf.fill((0, 0, 0, 0))
            pygame.draw.circle(self.surf, self.color, (self.shield_ring_radius, self.shield_ring_radius),
                               self.diameter // 2)
            self.surf.blit(self.shield_surf, (0, 0))