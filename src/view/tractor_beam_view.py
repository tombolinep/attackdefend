import math


class TractorBeamView:
    def __init__(self, model):
        self.model = model

    def draw(self, screen, start_point, end_point):
        dx, dy = end_point[0] - start_point[0], end_point[1] - start_point[1]
        angle = math.degrees(math.atan2(dy, dx)) - 90
        distance = math.hypot(dx, dy)

        rotated_surf = pygame.transform.rotate(self.model.surf, angle)
        scaled_surf = pygame.transform.scale(rotated_surf, (rotated_surf.get_width(), int(distance)))

        screen.blit(scaled_surf, start_point + pygame.math.Vector2(scaled_surf.get_size()) / 2)
