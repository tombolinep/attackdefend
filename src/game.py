import pygame
import random
from player import Player
from enemy import Enemy
from display import Display

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


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

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                elif event.type == pygame.QUIT:
                    self.running = False
                elif event.type == self.ADDENEMY:
                    new_enemy = Enemy(self.score)
                    self.enemies.add(new_enemy)
                    self.all_sprites.add(new_enemy)

            self.score += random.uniform(1, 1.8)
            self.screen.fill((0, 0, 0))

            Display.display_score(self.screen, self.score)

            for entity in self.all_sprites:
                self.screen.blit(entity.surf, entity.rect)

            if pygame.sprite.spritecollideany(self.player, self.enemies):
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
        pygame.quit()


if __name__ == "__main__":
    game_instance = Game()
    game_instance.run()
    game_instance.quit_game()
