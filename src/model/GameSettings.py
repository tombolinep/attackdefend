class GameSettings:
    def __init__(self):
        self.SCREEN_WIDTH = 1536
        self.SCREEN_HEIGHT = 864
        self.STATS_WIDTH = 350
        self.MAIN_GAME_WIDTH = self.SCREEN_WIDTH - self.STATS_WIDTH

    def update_screen_dimensions(self, width, height):
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        self.MAIN_GAME_WIDTH = self.SCREEN_WIDTH - self.STATS_WIDTH
