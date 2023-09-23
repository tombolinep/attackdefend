class ShieldView:
    def __init__(self, model):
        self.model = model

    def draw(self, screen):
        if self.model.player.attributes_bought.get('shield', 0) >= 1:
            image_rect = self.model.image.get_rect()
            image_rect.center = (self.model.diameter // 2, self.model.diameter // 2)
            self.model.surf.blit(self.model.image, image_rect.topleft)
            screen.blit(self.model.surf, self.model.rect.topleft)
