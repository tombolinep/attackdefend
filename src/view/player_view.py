import pygame
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH, MAIN_GAME_WIDTH


class PlayerView:

    def __init__(self, model):
        self.model = model
        self.SHIELD_COLORS = [(205, 127, 50), (192, 192, 192), (255, 223, 0), (0, 255, 255)]
        self._initialize_graphics()

    def _initialize_graphics(self):
        self.diameter = self.model.diameter
        self.shield_ring_radius = self.diameter // 2 + len(self.SHIELD_COLORS) * 5
        self.shield_surf = pygame.Surface((self.shield_ring_radius * 2, self.shield_ring_radius * 2), pygame.SRCALPHA)

    def render(self, screen):
        pygame.draw.circle(screen, self.model.color, (self.model.x, self.model.y), self.model.diameter // 2)
        self._draw_shield_rings(screen)

    def _draw_shield_rings(self, screen):
        for level in range(self.model.shield):
            ring_color = self.SHIELD_COLORS[level % len(self.SHIELD_COLORS)]
            ring_radius = self.diameter // 2 + (level + 1) * 5  # Increase the radius for each ring
            pygame.draw.circle(screen, ring_color, (self.model.x, self.model.y), ring_radius, 3)
