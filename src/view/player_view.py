import pygame


class PlayerView:
    def __init__(self, model):
        self.model = model
        self.SHIELD_COLORS = [(205, 127, 50), (192, 192, 192), (255, 223, 0), (0, 255, 255)]
        self.player_image = pygame.transform.scale(self.model.image, (self.model.rect.width, self.model.rect.height))
        self.player_rect = self.model.rect
        self.update_player_image()

    def render(self, screen):
        self.update_player_image()
        self.player_rect.center = (self.model.x, self.model.y)
        screen.blit(self.player_image, self.player_rect.topleft)

    def update_player_image(self):
        self.player_image = pygame.transform.scale(self.model.image, (self.model.rect.width, self.model.rect.height))
