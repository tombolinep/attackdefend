from pygame import mixer
from src.utils import resource_path


class Audio:
    def __init__(self):
        mixer.init()

        # Loading all the sound effects
        self.bg_music = mixer.Sound(resource_path('assets/tweakin.mp3'))
        self.death_sound = mixer.Sound(resource_path('assets/dead.mp3'))
        self.powerup_sound = mixer.Sound(resource_path('assets/powerup.mp3'))
        self.coin_sound = mixer.Sound(resource_path('assets/coin.mp3'))
        self.shield_hit_sound = mixer.Sound(resource_path('assets/shield_hit.mp3'))
        self.purchase_error_sound = mixer.Sound(resource_path('assets/purchase_error.wav'))
        self.purchase_success_sound = mixer.Sound(resource_path('assets/purchase_success.wav'))
        self.purchase_error_sound.set_volume(0.6)

        # Setting the volume for all the sound effects
        sound_effects = [
            self.bg_music,
            self.death_sound,
            self.powerup_sound,
            self.coin_sound,
            self.shield_hit_sound,
            self.purchase_success_sound
        ]
        for sound in sound_effects:
            sound.set_volume(0.1)  # Setting the volume to 0.2 for all sound files

    # The existing methods to play the respective sounds
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

    # New method to play the shield hit sound
    def play_shield_hit_sound(self):
        self.shield_hit_sound.play()

    def play_purchase_error_sound(self):
        self.purchase_error_sound.play()

    def play_purchase_success_sound(self):
        self.purchase_success_sound.play()
