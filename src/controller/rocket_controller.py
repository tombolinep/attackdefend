import pygame

from pygame.time import get_ticks


class RocketController:
    def __init__(self, model, view, settings):
        self.settings = settings
        self.model = model
        self.view = view

    def update(self):
        current_time = get_ticks()
        if not self.model.is_exploding:
            self.model.rect.x += self.model.dx * self.model.speed
            self.model.rect.y += self.model.dy * self.model.speed
            self.model.update_image_rotation()
            if current_time - self.model.start_time >= self.model.explosion_time:
                self.model.explode()
            elif self.is_out_of_bounds():
                self.model.kill()
        else:
            elapsed_time = current_time - self.model.start_time
            max_duration = self.model.explosion_duration
            max_size = self.model.explosion_radius * 2
            base_size = int(max_size * 0.6)

            growth_factor = 12
            new_size = int(base_size * (max_size / base_size) ** (growth_factor * elapsed_time / max_duration))
            new_size = min(new_size, max_size)

            self.model.image = pygame.transform.scale(self.model.explosion_image, (new_size, new_size))

            self.model.image.set_colorkey(self.model.image.get_at((new_size // 2, new_size - 1)))

            self.model.surf = self.model.image
            self.model.rect = self.model.surf.get_rect(center=self.model.rect.center)

            if current_time - self.model.start_time >= self.model.explosion_duration:
                self.model.kill()

    def is_out_of_bounds(self):
        return (self.model.rect.x < self.settings.STATS_WIDTH or self.model.rect.y < 0 or
                self.model.rect.x > self.settings.SCREEN_WIDTH or self.model.rect.y > self.settings.SCREEN_HEIGHT)
