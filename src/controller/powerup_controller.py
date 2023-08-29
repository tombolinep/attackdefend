class PowerUpController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def update(self):
        self.model.update_color()
