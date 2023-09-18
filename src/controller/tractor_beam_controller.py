import pygame


class TractorBeamController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update(self, screen):
        if not self.model.game_model.player.attributes_bought.get('tractor_beam_enabled') == 1:
            return

        player_center = (self.model.player.rect.centerx, self.model.player.rect.centery)

        for coin in self.model.game_model.coins:
            coin_center = (coin.rect.centerx, coin.rect.centery)
            distance = pygame.math.Vector2(coin_center) - pygame.math.Vector2(player_center)

            if 0 < distance.length() < self.model.range:
                unit_vector = distance.normalize()

                coin.rect.centerx -= unit_vector.x * self.model.pull_strength
                coin.rect.centery -= unit_vector.y * self.model.pull_strength

                self.view.draw(screen, player_center, coin_center)
