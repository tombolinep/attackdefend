from pygame.time import get_ticks


class RocketController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update(self):
        current_time = get_ticks()

        if not self.model.is_exploding:
            self.model.rect.x += self.model.dx * self.model.speed
            self.model.rect.y += self.model.dy * self.model.speed

            if current_time - self.model.start_time >= self.model.explosion_time:
                self.model.explode()
            elif self.model.is_out_of_bounds():
                self.model.kill()
        else:
            if current_time - self.model.start_time - self.model.explosion_time >= self.model.explosion_duration:
                self.model.kill()

        self.view.draw(self.model.screen)
