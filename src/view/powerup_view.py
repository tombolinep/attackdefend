import pygame


class PowerUpView:
    def __init__(self, model):
        self.model = model
        self.colors = [
            (255, 0, 0),  # Red
            (0, 255, 0),  # Green
            (0, 0, 255),  # Blue
            (255, 255, 0),  # Yellow
            (0, 255, 255),  # Cyan
            (255, 0, 255)  # Magenta
        ]

    def create_surface_with_color(self):
        color = self.colors[self.model.current_color_index]
        surf = pygame.Surface((self.model.width, self.model.height), pygame.SRCALPHA)

        # Draw lines with the given color
        pygame.draw.line(surf, color, (self.model.width // 2, 0), (self.model.width // 2, self.model.height), 3)
        pygame.draw.line(surf, color, (0, self.model.height // 2), (self.model.width, self.model.height // 2), 3)
        pygame.draw.line(surf, color, (0, 0), (self.model.width, self.model.height), 3)
        pygame.draw.line(surf, color, (0, self.model.height), (self.model.width, 0), 3)

        return surf

    def draw(self, screen, rect):
        surf = self.create_surface_with_color()
        screen.blit(surf, rect)
