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
        self.images['coin'] = pygame.image.load('assets/coin.png')
        self.images['junks'] = [pygame.image.load('assets/junk1.png'),
                                pygame.image.load('assets/junk2.png'),
                                pygame.image.load('assets/junk3.png')]
        self.images['player'] = pygame.image.load('assets/player.png')
        self.images['powerup'] = pygame.image.load('assets/powerup.png')
        self.images['background'] = pygame.image.load('assets/space_background.jpg')

        # Precompute junk variants
        for junk_image in self.images['junks']:
            for _ in range(10):  # creating 10 variants for each junk image
                self.junk_variants.append(self.get_rotated_image(junk_image))

        # Precompute coin variants
        for _ in range(10):  # creating 10 variants for the coin image
            self.coin_variants.append(self.get_scaled_coin_image())

    def get_image(self, image_key):
        return self.images.get(image_key)

    def get_random_junk_image(self):
        return random.choice(self.junk_variants)

    def get_rotated_image(self, image):
        angle = random.uniform(0, 360)
        return pygame.transform.rotate(image, angle)

    def get_random_coin_image(self):
        return random.choice(self.coin_variants)

    def get_scaled_coin_image(self, min_scale=0.8, max_scale=1.2):
        scale = random.uniform(min_scale, max_scale)
        width, height = self.images['coin'].get_size()
        width, height = int(width * scale), int(height * scale)
        return pygame.transform.scale(self.images['coin'], (width, height))
