from pygame import mixer
from src.utils import resource_path


class Audio:
    def __init__(self):
        mixer.init()
        self.bg_music = mixer.Sound(resource_path('assets/tweakin.mp3'))
        self.death_sound = mixer.Sound(resource_path('assets/dead.mp3'))
        self.powerup_sound = mixer.Sound(resource_path('assets/powerup.mp3'))
        self.coin_sound = mixer.Sound(resource_path('assets/coin.mp3'))
        self.bg_music.set_volume(0.1)

    def play_bg_music(self):
        self.bg_music.play(-1)

    def stop_bg_music(self):
        self.bg_music.stop()

    def play_death_sound(self):
        self.death_sound.play()

    def play_powerup_sound(self):
        self.powerup_sound.play()

    def play_coin_sound(self):
        self.coin_sound.play()
