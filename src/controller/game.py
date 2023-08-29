import pygame
import random
import math

from src.model.audio import Audio
from src.model.bullet import Bullet
from src.view.button import Button
from src.model.player import Player
from src.model.enemy import Enemy
from src.model.powerup import PowerUp
from src.view.display import Display
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, STATS_WIDTH, \
    MAIN_GAME_WIDTH, POWERUP_INTERVAL, COIN_INTERVAL
from src.model.shop import Shop
from src.model.coin import Coin


class Game:
    def __init__(self):
        self.initialize_pygame()
        self.initialize_events()
        self.initialize_game_attributes()
        self.initialize_music()
        self.initialize_ui_elements()

    def initialize_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

    def initialize_game_attributes(self):
        self.paused = False
        self.player = Player()
        self.enemies = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)
        self.running = True
        self.score = 0
        self.powerup_nice_font = pygame.font.Font(None, 36)
        self.powerup_nice_text = self.powerup_nice_font.render("Nice!", True, (255, 255, 255))
        self.display_nice_text = False
        self.next_powerup_time = pygame.time.get_ticks() + POWERUP_INTERVAL
        self.bought_timer = 0
        self.bought_message_position = (0, 0)

    def initialize_events(self):
        self.ADDENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ADDENEMY, 250)

        self.ADDPOWERUP = pygame.USEREVENT + 2
        pygame.time.set_timer(self.ADDPOWERUP, POWERUP_INTERVAL)

        self.ADDCOIN = pygame.USEREVENT + 3
        pygame.time.set_timer(self.ADDCOIN, COIN_INTERVAL)

        self.SHOOT = pygame.USEREVENT + 4
        pygame.time.set_timer(self.SHOOT, 4200)  # Fire every second

    def initialize_music(self):
        self.audio_manager = Audio()

    def initialize_ui_elements(self):
        self.pause_button = Button(SCREEN_WIDTH - 150, 10, 130, 40, "Pause", (150, 150, 150), (200, 200, 200))

    def run(self):
        self.audio_manager.play_bg_music()
        while self.running:
            self.handle_events()
            if not self.paused:
                self.update_game()
            self.draw_ui()
            pygame.display.flip()
            self.clock.tick(30)

    def draw_ui(self):
        self.pause_button.draw(self.screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == self.ADDENEMY:
                self.add_entity()
            elif event.type == self.ADDCOIN:
                self.add_coin()
            elif event.type == self.ADDPOWERUP:
                self.powerups.add(PowerUp())
                self.all_sprites.add(self.powerups)
                self.next_powerup_time = pygame.time.get_ticks() + POWERUP_INTERVAL
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.pause_button.is_hovered(pygame.mouse.get_pos()):
                    self.paused = not self.paused
                    self.pause_button.text = "Resume" if self.paused else "Pause"
                elif self.shop_button.is_hovered(pygame.mouse.get_pos()):

            elif event.type == self.SHOOT:
                self.shoot_bullet()

    def add_entity(self):
        if random.random() < 0.1:
            enemy_type = "red"
        else:
            enemy_type = "white"

        new_enemy = Enemy(self.score, enemy_type)
        self.enemies.add(new_enemy)
        self.all_sprites.add(new_enemy)

    def add_coin(self):
        coin_x = random.randint(STATS_WIDTH, SCREEN_WIDTH - 20)
        coin_y = random.randint(0, SCREEN_HEIGHT - 20)
        new_coin = Coin(coin_x, coin_y)
        self.coins.add(new_coin)
        self.all_sprites.add(new_coin)

    def add_powerup(self):
        new_powerup = PowerUp()
        self.powerups.add(new_powerup)
        self.all_sprites.add(new_powerup)
        self.next_powerup_time = pygame.time.get_ticks() + POWERUP_INTERVAL

    def update_game(self):
        self.score += random.uniform(1, 1.8)
        self.screen.fill((0, 0, 0))
        self.pause_button.draw(self.screen)

        pygame.draw.rect(self.screen, (200, 200, 200), (0, 0, STATS_WIDTH, SCREEN_HEIGHT))

        self.update_sprites()

        for powerup in self.powerups:
            if powerup.nice_text:
                text_surface = Display.create_text(powerup.nice_text, 24, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(powerup.rect.centerx, powerup.rect.centery - powerup.height))
                self.screen.blit(text_surface, text_rect)

        if len(self.enemies) > 0:
            total_enemy_speed = sum(enemy.speed for enemy in self.enemies)
            average_enemy_speed = total_enemy_speed / len(self.enemies)
        else:
            average_enemy_speed = 0

        Display.display_stats(self.screen, int(self.score), self.player.speed, average_enemy_speed,
                              self.next_powerup_time, self.player.coins)

        if self.display_nice_text:
            current_time = pygame.time.get_ticks()
            if current_time - self.nice_text_timer < 2000:
                text_surface = self.powerup_nice_text
                text_rect = text_surface.get_rect(center=self.nice_text_position)
                self.screen.blit(text_surface, text_rect)
            else:
                self.display_nice_text = False

        self.check_collisions()

        pressed_keys = pygame.key.get_pressed()
        self.player.update(pressed_keys)

    def update_sprites(self):
        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)
        self.enemies.update(self.player.rect)
        self.powerups.update()
        self.coins.update()
        self.player.draw(self.screen)
        self.bullets.update()  # Add this line

    def check_collisions(self):
        colliding_enemy = pygame.sprite.spritecollideany(self.player, self.enemies,
                                                         collided=self.collision_circle_rectangle)
        if colliding_enemy:
            self.handle_enemy_collision(colliding_enemy)

        colliding_powerup = pygame.sprite.spritecollideany(self.player, self.powerups)
        if colliding_powerup:
            self.handle_powerup_collision(colliding_powerup)

        colliding_coin = pygame.sprite.spritecollideany(self.player, self.coins)
        if colliding_coin:
            self.handle_coin_collision(colliding_coin)

        colliding_bullet_enemy = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        for enemy_list in colliding_bullet_enemy.values():
            for enemy in enemy_list:
                enemy.kill()

    def handle_enemy_collision(self, enemy):
        if self.player.get_shield() > 0:
            self.audio_manager.play_shield_hit_sound()
            self.player.remove_shield()
            enemy.kill()
        else:
            self.audio_manager.play_death_sound()
            should_restart = Display.display_game_over(self.screen)
            if should_restart:
                self.reset_game()
            else:
                self.running = False

    def handle_powerup_collision(self, powerup):
        self.audio_manager.play_powerup_sound()
        powerup.apply_powerup(self.enemies)
        powerup.kill()
        self.display_nice_text = True
        self.nice_text_timer = pygame.time.get_ticks()
        self.nice_text_position = powerup.rect.center

    def handle_coin_collision(self, coin):
        self.audio_manager.play_coin_sound()
        self.player.add_coin()
        coin.kill()

    def collision_circle_rectangle(self, circle_sprite, rectangle_sprite):
        dx = circle_sprite.rect.centerx - rectangle_sprite.rect.centerx
        dy = circle_sprite.rect.centery - rectangle_sprite.rect.centery

        closest_x = max(rectangle_sprite.rect.left, min(circle_sprite.rect.centerx, rectangle_sprite.rect.right))
        closest_y = max(rectangle_sprite.rect.top, min(circle_sprite.rect.centery, rectangle_sprite.rect.bottom))
        dist_x = circle_sprite.rect.centerx - closest_x
        dist_y = circle_sprite.rect.centery - closest_y

        return math.sqrt(dist_x ** 2 + dist_y ** 2) < circle_sprite.diameter / 2

    def reset_game(self):
        # self.player.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT )  # Reset player position
        self.enemies.empty()  # Clear enemies
        self.powerups.empty()  # Clear power-ups
        self.all_sprites.empty()  # Clear all sprites
        self.all_sprites.add(self.player)  # Add the player back to the sprites group
        self.score = 0  # Reset score
        self.next_powerup_time = pygame.time.get_ticks() + POWERUP_INTERVAL  # Reset power-up timer

    def quit_game(self):
        self.audio_manager.stop_bg_music()
        pygame.quit()

    def pause_timers(self):
        pygame.time.set_timer(self.ADDENEMY, 0)
        pygame.time.set_timer(self.ADDPOWERUP, 0)
        pygame.time.set_timer(self.ADDCOIN, 0)

    def resume_timers(self):
        pygame.time.set_timer(self.ADDENEMY, 250)
        pygame.time.set_timer(self.ADDPOWERUP, POWERUP_INTERVAL)
        pygame.time.set_timer(self.ADDCOIN, COIN_INTERVAL)

    def update_stats(self):
        # Clear the portion of the screen where the stats are displayed
        pygame.draw.rect(self.screen, (200, 200, 200), (0, 0, STATS_WIDTH, SCREEN_HEIGHT))

        if len(self.enemies) > 0:
            total_enemy_speed = sum(enemy.speed for enemy in self.enemies)
            average_enemy_speed = total_enemy_speed / len(self.enemies)
        else:
            average_enemy_speed = 0
        Display.display_stats(self.screen, int(self.score), self.player.speed, average_enemy_speed,
                              self.next_powerup_time, self.player.coins)

        # Optional: You might also want to refresh the display here
        pygame.display.flip()

    def shoot_bullet(self):
        closest_enemy = None
        closest_distance = float('inf')  # Initialize with a large value
        for enemy in self.enemies:
            distance = math.sqrt(
                (enemy.rect.centerx - self.player.rect.centerx) ** 2 +
                (enemy.rect.centery - self.player.rect.centery) ** 2
            )
            if distance < closest_distance:
                closest_enemy = enemy
                closest_distance = distance

        if closest_enemy:
            new_bullet = Bullet(
                self.player.rect.centerx,
                self.player.rect.centery,
                closest_enemy
            )
            self.bullets.add(new_bullet)
            self.all_sprites.add(new_bullet)


if __name__ == "__main__":
    game_instance = Game()
    game_instance.run()
    game_instance.quit_game()
