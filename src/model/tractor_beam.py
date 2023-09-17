import pygame


class TractorBeam(pygame.sprite.Sprite):
    def __init__(self, game_model):
        super().__init__()
        self.game_model = game_model
        self.range = 300
        self.pull_strength = 1
        self.screen = pygame.display.get_surface()

        self.surf = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        self.rect = self.surf.get_rect()

    def draw_cylinder(self, start_point, end_point, radius, color):
        dx, dy = end_point[0] - start_point[0], end_point[1] - start_point[1]
        distance = int(pygame.math.Vector2(dx, dy).length())
        segments = distance // radius

        for i in range(segments + 1):
            t = i / segments
            x = start_point[0] + t * dx
            y = start_point[1] + t * dy
            pygame.draw.circle(self.surf, color, (int(x), int(y)), radius)

    def update(self):
        if not self.game_model.player.attributes_bought.get('tractor_beam_enabled') == 1:
            return

        self.surf.fill((0, 0, 0, 0))  # Clearing the surface at the start of each update call

        for coin in self.game_model.coins:
            distance_x = self.game_model.player.x - coin.rect.x
            distance_y = self.game_model.player.y - coin.rect.y
            distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

            if distance < self.range:
                unit_vector_x = distance_x / distance
                unit_vector_y = distance_y / distance

                coin.x += unit_vector_x * self.pull_strength
                coin.y += unit_vector_y * self.pull_strength

                coin.rect.x = int(coin.x)
                coin.rect.y = int(coin.y)

                end_point = (coin.rect.x + coin.rect.width / 2, coin.rect.y + coin.rect.height / 2)
                start_point = (self.game_model.player.x, self.game_model.player.y)
                self.draw_cylinder(start_point, end_point, 10, (20, 200, 20, 20))
