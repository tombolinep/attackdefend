import random
import pygame


class ImageManager:
    def __init__(self):
        self.images = {}
        self.junk_variants = []
        self.coin_variants = []

    def load_images(self):
        self.images['bullet'] = pygame.image.load('assets/bullet.png')
        self.images['tractor_beam'] = pygame.image.load('assets/tractor_beam.png')
        self.images['enemy_red'] = pygame.image.load('assets/enemy_red.png')
        self.images['coins'] = [pygame.image.load('assets/coin_cyan.png'),
                                pygame.image.load('assets/coin_green.png'),
                                pygame.image.load('assets/coin_grey.png'),
                                pygame.image.load('assets/coin_peach.png'),
                                pygame.image.load('assets/coin_purple.png'),
                                pygame.image.load('assets/coin_red.png')]
        self.images['junks'] = [pygame.image.load('assets/junk1.png'),
                                pygame.image.load('assets/junk2.png'),
                                pygame.image.load('assets/junk3.png')]
        self.images['player'] = pygame.image.load('assets/player.png')
        self.images['powerup'] = pygame.image.load('assets/powerup.png')
        self.images['background'] = pygame.image.load('assets/space_background.jpg')
        self.images['rocket'] = pygame.image.load('assets/rocket.png')
        self.images['explosion'] = pygame.image.load('assets/explosion.png')
        self.images['laser'] = pygame.image.load('assets/laser_beam.png')

        self.cache_rotated_rockets()

        # Precompute junk variants
        for junk_image in self.images['junks']:
            for _ in range(10):  # creating 10 variants for each junk image
                self.junk_variants.append(self.get_rotated_image(junk_image))

        # Precompute coin variants
        for coin_image in self.images['coins']:
            for _ in range(10):  # creating 10 variants for each coin image
                self.coin_variants.append(coin_image)

    def get_image(self, image_key):
        return self.images.get(image_key)

    def get_random_junk_image(self):
        return random.choice(self.junk_variants)

    def get_random_coin_image(self):
        return random.choice(self.coin_variants)

    def get_rotated_image(self, image):
        angle = random.uniform(0, 360)
        return pygame.transform.rotate(image, angle)

    def cache_rotated_rockets(self):
        self.rotated_rockets = {}
        original_rocket = self.images['rocket']
        for angle in range(0, 360, 15):  # Creating cache for every 15 degrees
            rotated_image = pygame.transform.rotate(original_rocket, -angle)
            self.rotated_rockets[angle] = rotated_image
