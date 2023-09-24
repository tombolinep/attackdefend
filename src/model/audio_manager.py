from pygame import mixer
from utils import resource_path


class Audio:
    def __init__(self):
        mixer.init()

        self.bg_music = mixer.Sound(resource_path('assets/sounds/tweakin.mp3'))
        self.death_sound = mixer.Sound(resource_path('assets/sounds/dead.mp3'))
        self.powerup_sound = mixer.Sound(resource_path('assets/sounds/powerup.mp3'))
        self.coin_sound = mixer.Sound(resource_path('assets/sounds/coin.mp3'))
        self.shield_hit_sound = mixer.Sound(resource_path('assets/sounds/shield_hit.mp3'))
        self.purchase_error_sound = mixer.Sound(resource_path('assets/sounds/purchase_error.wav'))
        self.purchase_success_sound = mixer.Sound(resource_path('assets/sounds/purchase_success.wav'))
        self.rocket_launch = mixer.Sound(resource_path('assets/sounds/rocket_launch.mp3'))
        self.rocket_explosion = mixer.Sound(resource_path('assets/sounds/rocket_explosion.mp3'))
        self.bullet = mixer.Sound(resource_path('assets/sounds/bullet.wav'))
        self.laser = mixer.Sound(resource_path('assets/sounds/laser.wav'))
        self.junk_explosion = mixer.Sound(resource_path('assets/sounds/junk_explosion.wav'))
        self.enemy_explosion = mixer.Sound(resource_path('assets/sounds/enemy_explosion.wav'))

        self.purchase_error_sound.set_volume(0.4)
        self.rocket_launch.set_volume(0.7)
        self.rocket_explosion.set_volume(0.7)
        self.shield_hit_sound.set_volume(0.2)

        sound_effects = [
            self.bg_music,
            self.death_sound,
            self.powerup_sound,
            self.coin_sound,
            self.purchase_success_sound,
            self.bullet,
            self.junk_explosion,
            self.enemy_explosion,
            self.laser
        ]
        for sound in sound_effects:
            sound.set_volume(0.1)

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

    def play_shield_hit_sound(self):
        self.shield_hit_sound.play()

    def play_purchase_error_sound(self):
        self.purchase_error_sound.play()

    def play_purchase_success_sound(self):
        self.purchase_success_sound.play()

    def play_rocket_launch(self):
        self.rocket_launch.play()

    def play_rocket_explosion(self):
        self.rocket_explosion.play()

    def play_bullet_sound(self):
        self.bullet.play()

    def play_laser_sound(self):
        self.laser.play()

    def play_enemy_explosion(self):
        self.enemy_explosion.play()

    def play_junk_explosion(self):
        self.junk_explosion.play()