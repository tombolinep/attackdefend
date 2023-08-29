class EnemyController:
    def __init__(self, model):
        self.model = model

    def update(self):
        for enemy in self.model.sprites():
            enemy.update_position()
