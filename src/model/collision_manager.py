import pygame
import math


class CollisionManager:
    def __init__(self):
        pass

    def collision_circle_rectangle(self, circle_sprite, rectangle_sprite):
        dx = circle_sprite.rect.centerx - rectangle_sprite.rect.centerx
        dy = circle_sprite.rect.centery - rectangle_sprite.rect.centery

        closest_x = max(rectangle_sprite.rect.left, min(circle_sprite.rect.centerx, rectangle_sprite.rect.right))
        closest_y = max(rectangle_sprite.rect.top, min(circle_sprite.rect.centery, rectangle_sprite.rect.bottom))
        dist_x = circle_sprite.rect.centerx - closest_x
        dist_y = circle_sprite.rect.centery - closest_y

        return math.sqrt(dist_x ** 2 + dist_y ** 2) < circle_sprite.diameter / 2
