import pygame

from src.view.display_view import Display


class CollisionController:
    def __init__(self, model):
        self.model = model

    def check_collisions(self, player, enemies, powerups, coins, bullets):
        colliding_enemy = pygame.sprite.spritecollideany(player, enemies,
                                                         collided=self.model.collision_circle_rectangle)
        if colliding_enemy:
            self.handle_enemy_collision(player, colliding_enemy)

        colliding_powerup = pygame.sprite.spritecollideany(player, powerups)
        if colliding_powerup:
            self.handle_powerup_collision(colliding_powerup)

        colliding_coin = pygame.sprite.spritecollideany(player, coins)
        if colliding_coin:
            self.handle_coin_collision(colliding_coin)

        colliding_bullet_enemy = pygame.sprite.groupcollide(bullets, enemies, True, True)
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
