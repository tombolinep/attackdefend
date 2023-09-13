import math
import pygame
import pygame.gfxdraw


class CollisionController:
    def __init__(self, model, screen):
        self.model = model
        self.player = model.player
        self.enemies = model.enemies
        self.powerups = model.powerups
        self.coins = model.coins
        self.bullets = model.bullets
        self.rockets = model.rockets
        self.lasers = model.lasers
        self.audio_manager = model.audio_manager
        self.screen = screen
        self.running = model.running

    def collision_circle_circle(self, circle1, circle2):
        distance = math.sqrt((circle1['x'] - circle2['x']) ** 2 + (circle1['y'] - circle2['y']) ** 2)
        return distance <= ((circle1['diameter'] // 2) + (circle2['diameter'] // 2))

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

    def handle_rocket_collision(self, rocket):
        if rocket.is_exploding:
            for enemy in self.enemies.copy():
                if self.collision_circle_circle(
                        {'x': rocket.rect.centerx, 'y': rocket.rect.centery, 'diameter': 2 * rocket.explosion_radius},
                        {'x': enemy.rect.centerx, 'y': enemy.rect.centery, 'diameter': enemy.rect.width}):
                    enemy.kill()

    def handle_laser_collision(self, laser):
        laser_start = laser.start_point
        laser_end = laser.end_point

        for enemy in self.enemies.copy():
            enemy_rect = enemy.rect

            # Get the four corners of the enemy rectangle
            rect_points = [
                (enemy_rect.topleft),
                (enemy_rect.topright),
                (enemy_rect.bottomright),
                (enemy_rect.bottomleft),
            ]

            # Check each line segment of the rectangle for intersection with the laser line
            for i in range(4):
                segment_start, segment_end = rect_points[i], rect_points[(i + 1) % 4]
                if self.line_intersection(laser_start, laser_end, segment_start, segment_end):
                    enemy.kill()
                    break  # Exit loop early if a collision is detected

    def line_intersection(self, line1_start, line1_end, line2_start, line2_end):
        """Check if two line segments intersect"""
        # Convert lines to a general form Ax + By = C
        A1, B1 = line1_end[1] - line1_start[1], line1_start[0] - line1_end[0]
        C1 = A1 * line1_start[0] + B1 * line1_start[1]

        A2, B2 = line2_end[1] - line2_start[1], line2_start[0] - line2_end[0]
        C2 = A2 * line2_start[0] + B2 * line2_start[1]

        # Find the determinant
        det = A1 * B2 - A2 * B1
        if det == 0:  # Lines are parallel
            return False

        # Find the intersection point
        x = (B2 * C1 - B1 * C2) / det
        y = (A1 * C2 - A2 * C1) / det

        # Check if the intersection point is on both line segments
        is_on_line1 = (
                min(line1_start[0], line1_end[0]) <= x <= max(line1_start[0], line1_end[0])
                and min(line1_start[1], line1_end[1]) <= y <= max(line1_start[1], line1_end[1])
        )

        is_on_line2 = (
                min(line2_start[0], line2_end[0]) <= x <= max(line2_start[0], line2_end[0])
                and min(line2_start[1], line2_end[1]) <= y <= max(line2_start[1], line2_end[1])
        )

        return is_on_line1 and is_on_line2

    def check_collisions(self):
        for enemy in self.enemies:
            if self.collision_circle_rectangle(self.player, enemy.rect):
                self.handle_enemy_collision(enemy)

            if self.player.warp_field_enabled and self.player.is_point_in_warp_field(enemy.rect.center):
                enemy.in_warp_field = True
            else:
                enemy.in_warp_field = False

        for powerup in self.powerups:
            if self.collision_circle_rectangle(self.player, powerup.rect):
                self.handle_powerup_collision(powerup)

        for coin in self.coins:
            if self.collision_circle_rectangle(self.player, coin.rect):
                self.handle_coin_collision(coin)

        for rocket in self.rockets:
            self.handle_rocket_collision(rocket)

        for laser in self.lasers:
            self.handle_laser_collision(laser)

        colliding_bullet_enemy = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        for enemy_list in colliding_bullet_enemy.values():
            for enemy in enemy_list:
                enemy.kill()
