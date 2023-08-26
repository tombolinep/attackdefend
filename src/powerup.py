import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super(PowerUp, self).__init__()

        self.width = 50
        self.height = 50
        self.color = (128, 0, 128)  # Purple

        self.surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(self.surf, self.color, (0, 0, self.width, self.height))

        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    def apply_powerup(self, enemies_group):
        for enemy in enemies_group:
            enemy.kill()  # Remove all enemies from the group
