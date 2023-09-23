import pygame


class ShieldView:
    def __init__(self, model):
        self.model = model

    def draw(self, screen):
        print(self.model.player.attributes_bought.get('shield', 0))
        if self.model.player.attributes_bought.get('shield', 0) >= 1:
            print("actually drawing shield")
            self.model.surf.blit(self.model.image, (0, 0))
        screen.blit(self.model.surf, self.model.rect.topleft)
