import pygame
import random

from pygame import mixer

from player import Player
from enemy import Enemy
from display import Display

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
        self.bg_music = mixer.Sound('assets/tweakin.mp3')

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
                    enemy_type = "yellow" if random.random() < 0.1 else "white"  # 10% chance for yellow
                    new_enemy = Enemy(self.score, enemy_type)  # passing enemy_type as second argument to Enemy
                    self.enemies.add(new_enemy)
                    self.all_sprites.add(new_enemy)

            self.score += random.uniform(1, 1.8)
            self.screen.fill((0, 0, 0))

            # Fill stats area with a different background
            pygame.draw.rect(self.screen, (200, 200, 200), (0, 0, STATS_WIDTH, SCREEN_HEIGHT))

            # Render stats in the stats area
            Display.display_stats(self.screen, self.score, self.player.speed)

            for entity in self.all_sprites:
                self.screen.blit(entity.surf, entity.rect)

            colliding_enemy = pygame.sprite.spritecollideany(self.player, self.enemies)
            if colliding_enemy:
                if colliding_enemy.type == "yellow":
                    self.player.speed_up()
                    colliding_enemy.kill()
                else:
                    self.player.kill()
                    # Display game over screen
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
