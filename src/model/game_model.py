import math
import random
from math import sqrt

import pygame
from constants import POWERUP_INTERVAL, SCREEN_HEIGHT, BULLET_INTERVAL, \
    SCREEN_WIDTH, STATS_WIDTH, COIN_SIZE, POWERUP_SIZE, ENEMY_RED_CHANCE, RED_ENEMY_SPAWN_SCORE
from model.audio_manager import Audio
from model.bullet import Bullet
from model.coin import Coin
from model.enemy import Enemy
from model.image_manager import ImageManager
from model.laser import Laser
from model.player import Player
from model.powerup import PowerUp
from model.rocket import Rocket
from model.tractor_beam import TractorBeam
from model.warpfield import WarpField


class GameModel:
    def __init__(self):
        self.audio_manager = Audio()
        self.image_manager = ImageManager()
        self.image_manager.load_images()
        self.running = True
        self.paused = False
        self.score = 0
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.rockets = pygame.sprite.Group()
        self.lasers = pygame.sprite.Group()
        self.tractor_beams = pygame.sprite.Group()
        self.warp_fields = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.next_powerup_time = pygame.time.get_ticks() + POWERUP_INTERVAL
        self.next_bullet_time = pygame.time.get_ticks()
        self.game_over = False
        self.isPauseMenuVisible = False
        self.player = Player(self.image_manager)
        self.set_player(self.player)
        self.add_tractor_beam(TractorBeam(self, self.player, self.image_manager))
        self.add_warp_field(WarpField(self, self.player, self.image_manager))

    def set_game_over(self, game_over):
        self.game_over = game_over

    def reset_game(self):
        # Clear sprite groups
        self.enemies.empty()
        self.powerups.empty()
        self.coins.empty()
        self.bullets.empty()
        self.rockets.empty()
        self.lasers.empty()
        self.tractor_beams.empty()
        self.warp_fields.empty()

        # Re-add player to all_sprites
        self.all_sprites.empty()
        self.all_sprites.add(self.player)

        # Reset game-related variables
        self.score = 0
        self.next_powerup_time = pygame.time.get_ticks() + POWERUP_INTERVAL
        self.running = True
        self.game_over = False
        self.add_tractor_beam(TractorBeam(self, self.player, self.image_manager))
        self.add_warp_field(WarpField(self, self.player, self.image_manager))

    def set_player(self, player):
        self.player = player
        self.all_sprites.add(player)

    def add_enemy(self):
        enemy_type = "red" if random.random() < ENEMY_RED_CHANCE and self.score > RED_ENEMY_SPAWN_SCORE else "white"
        enemy = Enemy(self.score, self.player, self.image_manager, enemy_type)
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)

    def add_powerup(self):
        x = random.randint(STATS_WIDTH, SCREEN_WIDTH - POWERUP_SIZE)
        y = random.randint(0, SCREEN_HEIGHT - POWERUP_SIZE)
        powerup = PowerUp(x, y, self.image_manager)
        self.powerups.add(powerup)
        self.all_sprites.add(powerup)

    def add_coin(self):
        x = random.randint(STATS_WIDTH, SCREEN_WIDTH - COIN_SIZE)
        y = random.randint(0, SCREEN_HEIGHT - COIN_SIZE)
        coin = Coin(x, y, self.image_manager)
        self.coins.add(coin)
        self.all_sprites.add(coin)

    def spawn_coin_at_location(self, x, y):
        new_coin = Coin(x, y, self.image_manager)
        self.coins.add(new_coin)
        self.all_sprites.add(new_coin)

    def add_bullet(self, bullet):
        self.bullets.add(bullet)
        self.all_sprites.add(bullet)

    def add_rocket(self, rocket):
        self.rockets.add(rocket)
        self.all_sprites.add(rocket)

    def add_laser(self, laser):
        self.lasers.add(laser)
        self.all_sprites.add(laser)

    def add_tractor_beam(self, tractor_beam):
        self.tractor_beams.add(tractor_beam)
        self.all_sprites.add(tractor_beam)

    def add_warp_field(self, warp_field):
        self.warp_fields.add(warp_field)
        self.all_sprites.add(warp_field)

    def increment_score(self):
        self.score += 1

    def find_closest_enemy(self):
        closest_enemy = None
        closest_distance = float("inf")

        for enemy in self.enemies:
            dx = enemy.rect.x - self.player.x
            dy = enemy.rect.y - self.player.y
            distance = sqrt(dx ** 2 + dy ** 2)

            if distance < closest_distance:
                closest_distance = distance
                closest_enemy = enemy

        return closest_enemy

    def calculate_target(self, closest_enemy):
        dx = closest_enemy.rect.x - self.player.x
        dy = closest_enemy.rect.y - self.player.y

        scale = SCREEN_HEIGHT / (abs(dy) + 1e-6)

        target_x = self.player.x + dx * scale
        target_y = self.player.y + dy * scale

        return target_x, target_y

    def automatic_shoot(self):
        current_time = pygame.time.get_ticks()
        rapid_charge_system_count = self.player.attributes_bought.get('reload_speed', 0)
        adjusted_bullet_interval = BULLET_INTERVAL - (500 * rapid_charge_system_count)
        num_of_guns = self.player.num_of_guns

        if current_time >= self.next_bullet_time:
            closest_enemy = self.find_closest_enemy()

            if closest_enemy:
                target_x, target_y = self.calculate_target(closest_enemy)

                for i in range(num_of_guns):
                    angle_offset = math.radians(i * 10 - (5 * (num_of_guns - 1)))

                    bullet = Bullet(self.player.x + (i * 20 - (10 * (num_of_guns - 1))),
                                    self.player.y + (i * 10 - (5 * (num_of_guns - 1))),
                                    target_x, target_y, self.image_manager)
                    bullet.adjust_trajectory(angle_offset)
                    self.add_bullet(bullet)

            self.next_bullet_time = current_time + adjusted_bullet_interval

    def rocket_shoot(self):
        if self.player.attributes_bought.get('rocket_launcher_enabled'):
            target_x, target_y = self.calculate_highest_enemy_density_target()
            new_rocket = Rocket(self.player.x, self.player.y, target_x, target_y, self.audio_manager,
                                self.image_manager)
            self.add_rocket(new_rocket)
            self.audio_manager.play_rocket_launch()

    def laser_shoot(self):
        if self.player.attributes_bought.get('laser_enabled'):
            enemy = self.find_random_enemy()
            if enemy:
                new_laser_beam = Laser(self.player, enemy.rect, self.audio_manager, self.image_manager)
                self.add_laser(new_laser_beam)

    @staticmethod
    def calculate_average_enemy_speed(enemies):
        if len(enemies) > 0:
            total_enemy_speed = sum(enemy.speed for enemy in enemies)
            return round(total_enemy_speed / len(enemies), 2)
        else:
            return 0

    def find_random_enemy(self):
        all_enemies = [e for e in self.all_sprites if isinstance(e, Enemy)]
        if all_enemies:
            return random.choice(all_enemies)

    def calculate_highest_enemy_density_target(self):
        grid_size = 100  # Define the size of each grid cell
        cols = (SCREEN_WIDTH - STATS_WIDTH) // grid_size
        rows = SCREEN_HEIGHT // grid_size

        # Create a 2D list to hold the number of enemies in each cell
        grid = [[0 for _ in range(cols)] for _ in range(rows)]

        # Iterate over each enemy and increment the count in the corresponding cell
        for enemy in self.enemies:
            col = (enemy.rect.x - STATS_WIDTH) // grid_size
            row = enemy.rect.y // grid_size
            col = max(0, min(col, cols - 1))
            row = max(0, min(row, rows - 1))
            grid[row][col] += 1

        # Find the cell with the highest enemy density
        max_density = max(max(row) for row in grid)
        target_row, target_col = next(
            (r, c) for r, row in enumerate(grid) for c, val in enumerate(row) if val == max_density)

        # Calculate the target coordinates as the center of this cell
        target_x = STATS_WIDTH + target_col * grid_size + grid_size // 2
        target_y = target_row * grid_size + grid_size // 2

        return target_x, target_y
