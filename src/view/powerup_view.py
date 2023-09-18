class PowerUpView:
    def __init__(self, model):
        self.model = model

    def draw(self, screen):
        screen.blit(self.model.image, self.model.rect)
