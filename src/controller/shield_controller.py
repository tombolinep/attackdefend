import pygame


class ShieldController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update(self):
        if self.model.player.attributes_bought.get('shield', 0) >= 1:
            self.model.update_diameter_and_surface()

            self.model.x = self.model.player.rect.centerx
            self.model.y = self.model.player.rect.centery
            self.model.rect.center = (self.model.x, self.model.y)
            self.view.draw(self.model.screen)
