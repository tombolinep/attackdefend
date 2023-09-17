import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH, MAIN_GAME_WIDTH


class PlayerView:
    def __init__(self, model):
        self.model = model
        self.SHIELD_COLORS = [(205, 127, 50), (192, 192, 192), (255, 223, 0), (0, 255, 255)]
        self.player_image = pygame.transform.scale(self.model.image, (self.model.rect.width, self.model.rect.height))
        self.player_rect = self.model.rect
        self.shield_ring_radius = self.model.rect.width // 2 + len(self.SHIELD_COLORS) * 5
        self.shield_surf = pygame.Surface((self.shield_ring_radius * 2, self.shield_ring_radius * 2), pygame.SRCALPHA)
        self.update_player_image()

    def render(self, screen):
        self.update_player_image()
        self.player_rect.center = (self.model.x, self.model.y)
        screen.blit(self.player_image, self.player_rect.topleft)
        self._draw_shield_rings(screen)
        self._draw_warp_field(screen)

    def _draw_shield_rings(self, screen):
        for level in range(self.model.shield):
            ring_color = self.SHIELD_COLORS[level % len(self.SHIELD_COLORS)]
            ring_radius = self.model.rect.width // 2 + (level + 1) * 5
            pygame.draw.circle(screen, ring_color, self.player_rect.center, ring_radius, 3)

    def _draw_warp_field(self, screen):
        if self.model.warp_field_enabled:
            warp_field_color = (0, 255, 255, 64)
            warp_field_radius = 100
            warp_field_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            pygame.draw.circle(warp_field_surface, warp_field_color, (self.model.x, self.model.y), warp_field_radius)
            screen.blit(warp_field_surface, (0, 0))

    def update_player_image(self):
        self.player_image = pygame.transform.scale(self.model.image, (self.model.rect.width, self.model.rect.height))
        self.shield_ring_radius = self.model.rect.width // 2 + len(self.SHIELD_COLORS) * 5

    def update_shield_rings(self):
        self.shield_ring_radius = self.player_rect.width // 2 + len(self.SHIELD_COLORS) * 5
