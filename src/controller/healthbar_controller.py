class HealthBarController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update_health(self, new_health):
        self.model.set_health(new_health)

    def update(self, screen):
        health_ratio = self.model.get_health_ratio()
        self.view.draw(self.model.surf, 0, 0, health_ratio)  # Drawing onto self.model.surf
        screen.blit(self.model.surf, self.model.rect.topleft)
