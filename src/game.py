import pygame
import random
import math

from utils import resource_path
from pygame import mixer
from player import Player
from enemy import Enemy
from powerup import PowerUp
from display import Display
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH, MAIN_GAME_WIDTH, POWERUP_INTERVAL


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.player = Player()
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()  # Create a group for power-ups
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        self.running = True
        self.score = 0

        self.ADDENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADDENEMY, 250)

        self.ADDPOWERUP = pygame.USEREVENT + 2  # Add a new user event for power-ups
        pygame.time.set_timer(self.ADDPOWERUP, POWERUP_INTERVAL)  # Set the timer for adding power-ups (15 seconds)

        self.next_powerup_time = 0  # Initialize the time for the next power-up
        self.POWERUP_INTERVAL = POWERUP_INTERVAL  # Interval for power-up in milliseconds (15 seconds)

        mixer.init()
        self.bg_music = mixer.Sound(resource_path('assets/tweakin.mp3'))

    def run(self):
        self.next_powerup_time = pygame.time.get_ticks() + self.POWERUP_INTERVAL
        self.bg_music.play(-1)
        while self.running:
            self.handle_events()
            self.update_game()
            pygame.display.flip()
            self.clock.tick(30)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.QUIT:
                self.running = False
            elif event.type == self.ADDENEMY:
                self.add_enemy()
            elif event.type == self.ADDPOWERUP:
                self.add_powerup()

    def add_enemy(self):
        if random.random() < 0.1:
            enemy_type = "yellow"
        elif random.random() < 0.03:
            enemy_type = "red"
        else:
            enemy_type = "white"

        new_enemy = Enemy(self.score, enemy_type)
        self.enemies.add(new_enemy)
        self.all_sprites.add(new_enemy)

    def add_powerup(self):
        new_powerup = PowerUp()
        self.powerups.add(new_powerup)
        self.all_sprites.add(new_powerup)
        self.next_powerup_time = pygame.time.get_ticks() + self.POWERUP_INTERVAL

    def update_game(self):
        self.score += random.uniform(1, 1.8)
        self.screen.fill((0, 0, 0))

        pygame.draw.rect(self.screen, (200, 200, 200), (0, 0, STATS_WIDTH, SCREEN_HEIGHT))

        self.update_sprites()

        if len(self.enemies) > 0:
            total_enemy_speed = sum(enemy.speed for enemy in self.enemies)
            average_enemy_speed = total_enemy_speed / len(self.enemies)
        else:
            average_enemy_speed = 0

        Display.display_stats(self.screen, int(self.score), self.player.speed, average_enemy_speed,
                              self.next_powerup_time)  # Pass the next_powerup_time

        self.check_collisions()

        pressed_keys = pygame.key.get_pressed()
        self.player.update(pressed_keys)

    def update_sprites(self):
        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)
        self.enemies.update()
        self.powerups.update()  # Update power-ups

    def check_collisions(self):
        colliding_enemy = pygame.sprite.spritecollideany(self.player, self.enemies,
                                                         collided=self.collision_circle_rectangle)
        if colliding_enemy:
            self.handle_enemy_collision(colliding_enemy)

        colliding_powerup = pygame.sprite.spritecollideany(self.player, self.powerups)  # Check power-up collision
        if colliding_powerup:
            self.handle_powerup_collision(colliding_powerup)

    def handle_enemy_collision(self, enemy):
        if enemy.type == "yellow":
            self.player.speed_up()
            enemy.kill()
        elif enemy.type == "red":
            for enemy in self.enemies:
                enemy.speed_up_temporarily()
            enemy.kill()
        else:
            should_restart = Display.display_game_over(self.screen)
            if should_restart:
                self.reset_game()
            else:
                self.running = False

    def handle_powerup_collision(self, powerup):
        powerup.apply_powerup(self.enemies)  # Apply power-up effect
        powerup.kill()  # Remove the power-up

    def collision_circle_rectangle(self, circle_sprite, rectangle_sprite):
        dx = circle_sprite.rect.centerx - rectangle_sprite.rect.centerx
        dy = circle_sprite.rect.centery - rectangle_sprite.rect.centery

        closest_x = max(rectangle_sprite.rect.left, min(circle_sprite.rect.centerx, rectangle_sprite.rect.right))
        closest_y = max(rectangle_sprite.rect.top, min(circle_sprite.rect.centery, rectangle_sprite.rect.bottom))
        dist_x = circle_sprite.rect.centerx - closest_x
        dist_y = circle_sprite.rect.centery - closest_y

        return math.sqrt(dist_x ** 2 + dist_y ** 2) < circle_sprite.diameter / 2

    def reset_game(self):
        self.player = Player()
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()  # Reset power-ups group
        self.all_sprites.add(self.player)
        self.score = 0
        self.next_powerup_time = pygame.time.get_ticks() + self.POWERUP_INTERVAL  # Reset power-up timer

    def quit_game(self):
        self.bg_music.stop()
        pygame.quit()


if __name__ == "__main__":
    game_instance = Game()
    game_instance.run()
    game_instance.quit_game()
