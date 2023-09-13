import pygame


class TractorBeam(pygame.sprite.Sprite):
    def __init__(self, game_model):
        super().__init__()
        self.game_model = game_model
        self.range = 300
        self.pull_strength = 1

    def update(self):
        if not self.game_model.player.attributes_bought.get('tractor_beam_enabled') == 1:
            return

        for coin in self.game_model.coins:
            distance_x = self.game_model.player.x - coin.rect.x
            distance_y = self.game_model.player.y - coin.rect.y
            distance = (distance_x**2 + distance_y**2)**0.5

            print(f"Distance to coin: {distance}")  # Debugging line

            if distance < self.range:
                # Calculate the unit vector towards the player
                unit_vector_x = distance_x / distance
                unit_vector_y = distance_y / distance

                # Debugging lines
                print(f"Unit vector: ({unit_vector_x}, {unit_vector_y})")
                print(f"Before update: (x, y) = ({coin.rect.x}, {coin.rect.y})")

                coin.x += unit_vector_x * self.pull_strength
                coin.y += unit_vector_y * self.pull_strength

                # Update the coin's screen position based on its new logical position
                coin.rect.x = int(coin.x)
                coin.rect.y = int(coin.y)
