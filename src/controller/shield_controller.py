import pygame


class ShieldController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update(self):
        if self.model.player.attributes_bought.get('shield', 0) >= 1:
            # Update the diameter and surface based on the player's size first
            self.model.update_diameter_and_surface()

            # Then update the shield's position to match the player's new center
            self.model.x = self.model.player.rect.centerx
            self.model.y = self.model.player.rect.centery

            # Update the shield's rect to the new center position
            self.model.rect.center = (self.model.x, self.model.y)

            # Draw the shield on the screen
            self.view.draw(self.model.screen)