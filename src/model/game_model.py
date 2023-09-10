import math
import random
from math import sqrt

import pygame
from src.constants import POWERUP_INTERVAL, SCREEN_HEIGHT, BULLET_INTERVAL, \
    SCREEN_WIDTH, STATS_WIDTH, COIN_SIZE, POWERUP_SIZE
from src.model.audio_manager import Audio
from src.model.bullet import Bullet
from src.model.coin import Coin
from src.model.enemy import Enemy
from src.model.powerup import PowerUp
from src.model.rocket import Rocket


class GameModel:
    def __init__(self):
        self.audio_manager = Audio()
        self.running = True
        self.paused = False
        self.score = 0
        self.player = None
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.rockets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.next_powerup_time = pygame.time.get_ticks() + POWERUP_INTERVAL
        self.next_bullet_time = pygame.time.get_ticks()
        self.game_over = False
        self.isPauseMenuVisible = False

    def stop_game(self):
        self.running = False

    def set_game_over(self, game_over):
        self.game_over = game_over

    def toggle_pause(self):
        self.paused = not self.paused

    def set_pause(self, pause_state):
        self.paused = pause_state

    def reset_game(self):
        # Clear sprite groups
        self.enemies.empty()
        self.powerups.empty()
        self.coins.empty()
        self.bullets.empty()
        self.rockets.empty()

        # Re-add player to all_sprites
        self.all_sprites.empty()
        self.all_sprites.add(self.player)

        # Reset game-related variables
        self.score = 0
        self.next_powerup_time = pygame.time.get_ticks() + POWERUP_INTERVAL
        self.running = True
        self.game_over = False

    def set_player(self, player):
        self.player = player
        self.all_sprites.add(player)

    def add_enemy(self):
        enemy_type = "red" if random.random() < 0.1 else "white"
        enemy = Enemy(self.score, enemy_type)
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)

    def add_powerup(self):
        x = random.randint(STATS_WIDTH, SCREEN_WIDTH - POWERUP_SIZE)
        y = random.randint(0, SCREEN_HEIGHT - POWERUP_SIZE)
        powerup = PowerUp(x, y)
        self.powerups.add(powerup)
        self.all_sprites.add(powerup)

    def add_coin(self):
        x = random.randint(STATS_WIDTH, SCREEN_WIDTH - COIN_SIZE)
        y = random.randint(0, SCREEN_HEIGHT - COIN_SIZE)
        coin = Coin(x, y)
        self.coins.add(coin)
        self.all_sprites.add(coin)

    def add_bullet(self, bullet):
        self.bullets.add(bullet)
        self.all_sprites.add(bullet)

    def add_rocket(self, rocket):
        self.bullets.add(rocket)
        self.all_sprites.add(rocket)

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

        if dy == 0:  # Add this check to avoid division by zero
            dy = 1  # or some small value to prevent division by zero

        scale = SCREEN_HEIGHT / abs(dy)

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
                                    target_x, target_y)
                    bullet.adjust_trajectory(angle_offset)
                    self.add_bullet(bullet)

            self.next_bullet_time = current_time + adjusted_bullet_interval

    def rocket_shoot(self):
        if self.player.attributes_bought.get('rocket_launcher_enabled'):
            target_x, target_y = self.calculate_highest_enemy_density_target()
            new_rocket = Rocket(self.player.x, self.player.y, target_x, target_y)
            self.add_rocket(new_rocket)

    @staticmethod
    def calculate_time_until_powerup(next_powerup_time):
        current_time = pygame.time.get_ticks()
        return max(0, (next_powerup_time - current_time) // 1000)

    @staticmethod
    def calculate_average_enemy_speed(enemies):
        if len(enemies) > 0:
            total_enemy_speed = sum(enemy.speed for enemy in enemies)
            return round(total_enemy_speed / len(enemies), 2)
        else:
            return 0

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
        target_row, target_col = next((r, c) for r, row in enumerate(grid) for c, val in enumerate(row) if val == max_density)

        # Calculate the target coordinates as the center of this cell
        target_x = STATS_WIDTH + target_col * grid_size + grid_size // 2
        target_y = target_row * grid_size + grid_size // 2

        return target_x, target_y
