# Import the pygame module
import pygame
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def display_game_over(screen):
    font = pygame.font.Font(None, 74)
    text_surface = font.render('Game Over', True, (255, 0, 0))
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))

    instruction_font = pygame.font.Font(None, 36)
    instruction_surface = instruction_font.render('Press R to Retry or Q to Quit', True, (255, 255, 255))
    instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))

    screen.blit(text_surface, text_rect)
    screen.blit(instruction_surface, instruction_rect)

    pygame.display.flip()

    game_over = True
    while game_over:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == pygame.K_r:  # Retry
                    return True
                if event.key == pygame.K_q or event.key == K_ESCAPE:  # Quit
                    return False
            elif event.type == QUIT:
                return False


# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()

        # Define the circle's diameter and color
        self.diameter = 75
        self.color = (0, 0, 255)  # Blue

        # Create a surface with the size of the circle's diameter
        self.surf = pygame.Surface((self.diameter, self.diameter), pygame.SRCALPHA)  # SRCALPHA for transparency

        # Draw a blue circle on the surface
        pygame.draw.circle(self.surf, self.color, (self.diameter // 2, self.diameter // 2), self.diameter // 2)

        # Get the rectangle of the surface for positioning
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -15)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 15)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-15, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(15, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

            # Define the enemy object by extending pygame.sprite.Sprite


# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(1, 5)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


# Initialize pygame
pygame.init()
clock = pygame.time.Clock()

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

# Instantiate player. Right now, this is just a rectangle.
player = Player()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Variable to keep the main loop running
running = True

# Main loop
while running:
    # for loop through the event queue
    for event in pygame.event.get():
        # Check for KEYDOWN event
        if event.type == KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False

        # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    # Fill the screen with black
    screen.fill((0, 0, 0))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, then remove the player
        player.kill()
        # Display game over screen
        should_restart = display_game_over(screen)
        if should_restart:
            player = Player()
            all_sprites = pygame.sprite.Group()
            enemies = pygame.sprite.Group()
            all_sprites.add(player)
        else:
            running = False

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    # Update enemy position
    enemies.update()

    # Update the display
    pygame.display.flip()
    clock.tick(30)
