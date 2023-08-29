from src.constants import SCREEN_HEIGHT


class BulletController:
    def __init__(self, model):
        self.model = model

    def update(self):
        self.model.rect.x += self.model.dx * self.model.speed
        self.model.rect.y += self.model.dy * self.model.speed

        if self.model.rect.bottom < 0 or self.model.rect.top > SCREEN_HEIGHT:
            return "kill"
        return None
