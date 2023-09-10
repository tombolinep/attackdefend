import math
import pygame


class CollisionController:
    def __init__(self, model, screen):
        self.model = model
        self.player = model.player
        self.enemies = model.enemies
        self.powerups = model.powerups
        self.coins = model.coins
        self.bullets = model.bullets
        self.rockets = model.rockets
        self.audio_manager = model.audio_manager
        self.screen = screen
        self.running = model.running

    def collision_circle_circle(self, circle1, circle2):
        distance = math.sqrt((circle1.x - circle2.x) ** 2 + (circle1.y - circle2.y) ** 2)
        return distance <= (circle1.diameter // 2 + circle2.diameter // 2)

    def handle_rocket_collision(self, rocket):
        blast_radius = 2500  # Define the blast radius

        for enemy in self.enemies.copy():  # Copy the list to avoid modifying it while iterating
            if self.collision_circle_circle(rocket, enemy):
                # Check if the enemy is within the blast radius
                distance = math.sqrt((rocket.x - enemy.x) ** 2 + (rocket.y - enemy.y) ** 2)
                if distance <= blast_radius:
                    enemy.kill()

        # Draw the blast radius for visualization
        pygame.draw.circle(self.screen, (255, 0, 0), (int(rocket.x), int(rocket.y)), blast_radius, 1)

    def collision_circle_rectangle(self, circle, rect):
        circle_distance_x = abs(circle.x - rect.x - rect.width // 2)
        circle_distance_y = abs(circle.y - rect.y - rect.height // 2)

        # If the circle and rectangle are far enough apart to not overlap, return False
        if circle_distance_x > (rect.width // 2 + circle.diameter // 2):
            return False
        if circle_distance_y > (rect.height // 2 + circle.diameter // 2):
            return False

        # If the circle's center is inside the rectangle, then they are colliding
        if circle_distance_x <= (rect.width // 2):
            return True
        if circle_distance_y <= (rect.height // 2):
            return True

        # Check for collision at rectangle corner.
        corner_distance_sq = (circle_distance_x - rect.width // 2) ** 2 + (circle_distance_y - rect.height // 2) ** 2

        return corner_distance_sq <= (circle.diameter // 2) ** 2

    def handle_enemy_collision(self, enemy):
        if self.player.shield > 0:
            self.audio_manager.play_shield_hit_sound()
            self.player.update_attribute(attribute='shield', action='decrease', change_amount=1)
            enemy.kill()
        else:
            self.audio_manager.play_death_sound()
            self.model.set_game_over(True)

    def handle_powerup_collision(self, powerup):
        self.audio_manager.play_powerup_sound()
        powerup.apply_powerup(self.enemies)
        powerup.kill()

    def handle_coin_collision(self, coin):
        self.audio_manager.play_coin_sound()
        self.player.add_coin()
        coin.kill()

    def check_collisions(self):
        for enemy in self.enemies:
            if self.collision_circle_rectangle(self.player, enemy.rect):
                self.handle_enemy_collision(enemy)

        for powerup in self.powerups:
            if self.collision_circle_rectangle(self.player, powerup.rect):
                self.handle_powerup_collision(powerup)

        for coin in self.coins:
            if self.collision_circle_rectangle(self.player, coin.rect):
                self.handle_coin_collision(coin)

        for rocket in self.rockets:
            self.handle_rocket_collision(rocket)

        colliding_bullet_enemy = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        for enemy_list in colliding_bullet_enemy.values():
            for enemy in enemy_list:
                enemy.kill()