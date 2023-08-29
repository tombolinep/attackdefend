import pygame


class EnemyView:
    def __init__(self, model):
        self.model = model
        self.surf = pygame.Surface((20, 10))
        if self.model.type == "red":
            self.surf.fill((255, 0, 0))
        else:
            self.surf.fill((255, 255, 255))

    def draw(self, screen):
        screen.blit(self.surf, self.model.rect.topleft)
