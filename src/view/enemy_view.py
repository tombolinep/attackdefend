import pygame


class EnemyView:
    def __init__(self, model):
        self.model = model

    def draw(self, screen):
        # Draw the enemy sprite
        screen.blit(self.model.surf, self.model.rect.topleft)

        # Update the health bar position based on the enemy position
        self.model.health_controller.set_position(self.model.rect.x, self.model.rect.bottom + 5)

        # Draw the health bar
        self.model.health_controller.draw(screen)
