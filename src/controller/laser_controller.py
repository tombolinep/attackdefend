class LaserController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update(self):
        current_time = get_ticks()
        if self.model.is_shooting:
            if current_time - self.model.start_time < self.model.duration:
                self.shoot()
            else:
                self.model.is_shooting = False
                self.model.kill()

    def shoot(self):
        self.model.start_point = (self.model.player.x, self.model.player.y)
        self.model.end_point = (self.model.target.x + self.model.target.width / 2, self.model.target.y + self.model.target.height / 2)
        self.model.calculate_trajectory()