class EnemyController:
    def __init__(self, model):
        self.model = model

    def update(self, player_center=None):
        self.model.update_position()
