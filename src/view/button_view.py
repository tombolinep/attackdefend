import pygame


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)  # Define the button's rect
        self.text = text
        self.color = color
        self.hover_color = hover_color

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)  # Check collision with rect

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.is_hovered(pygame.mouse.get_pos())
        return False

    def draw(self, screen):
        if self.is_hovered(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, self.hover_color, self.rect)  # Use rect
        else:
            pygame.draw.rect(screen, self.color, self.rect)  # Use rect

        font = pygame.font.SysFont(None, 36)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)  # Use rect center
        screen.blit(text_surface, text_rect)
