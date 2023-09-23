import pygame


class WarpFieldController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update(self):
        if self.model.game_model.player.attributes_bought.get('warp_field_enabled') == 1:
            self.model.x = self.model.player.rect.centerx
            self.model.y = self.model.player.rect.centery
            self.model.rect.center = (self.model.x, self.model.y)
            self.view.draw(self.model.screen)
