# button_view.py

import pygame


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = hover_color

    def is_hovered(self, mouse_pos):
        return self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.is_hovered(pygame.mouse.get_pos())
        return False

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.is_hovered(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        font = pygame.font.SysFont(None, 36)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)
