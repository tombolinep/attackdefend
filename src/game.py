import pygame
import random
import math

from pygame import mixer

from player import Player
from enemy import Enemy
from display import Display
from utils import resource_path

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH, MAIN_GAME_WIDTH


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.player = Player()
        self.enemies = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        self.running = True
        self.score = 0

        self.ADDENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADDENEMY, 250)

        mixer.init()
        self.bg_music = mixer.Sound(resource_path('assets/tweakin.mp3'))

    def run(self):
        self.bg_music.play(-1)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                elif event.type == pygame.QUIT:
                    self.running = False

                elif event.type == self.ADDENEMY:
                    if random.random() < 0.1:
                        enemy_type = "yellow"
                    elif random.random() < 0.03:
                        enemy_type = "red"
                    else:
                        enemy_type = "white"

                    new_enemy = Enemy(self.score, enemy_type)
                    self.enemies.add(new_enemy)
                    self.all_sprites.add(new_enemy)

            self.score += random.uniform(1, 1.8)
            self.screen.fill((0, 0, 0))

            pygame.draw.rect(self.screen, (200, 200, 200), (0, 0, STATS_WIDTH, SCREEN_HEIGHT))

            for entity in self.all_sprites:
                self.screen.blit(entity.surf, entity.rect)

            if len(self.enemies) > 0:
                total_enemy_speed = sum(enemy.speed for enemy in self.enemies)
                average_enemy_speed = total_enemy_speed / len(self.enemies)
            else:
                average_enemy_speed = 0

            Display.display_stats(self.screen, int(self.score), self.player.speed, average_enemy_speed)

            colliding_enemy = pygame.sprite.spritecollideany(self.player, self.enemies,
                                                             collided=self.collision_circle_rectangle)
            if colliding_enemy:
                if colliding_enemy.type == "yellow":
                    self.player.speed_up()
                    colliding_enemy.kill()
                elif colliding_enemy.type == "red":
                    for enemy in self.enemies:
                        enemy.speed_up_temporarily()
                    colliding_enemy.kill()
                else:
                    self.player.kill()
                    should_restart = Display.display_game_over(self.screen)
                    if should_restart:
                        self.reset_game()
                    else:
                        self.running = False

            pressed_keys = pygame.key.get_pressed()
            self.player.update(pressed_keys)
            self.enemies.update()
            pygame.display.flip()
            self.clock.tick(30)

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
        self.all_sprites.add(self.player)
        self.score = 0

    def quit_game(self):
        self.bg_music.stop()
        pygame.quit()


if __name__ == "__main__":
    game_instance = Game()
    game_instance.run()
    game_instance.quit_game()
