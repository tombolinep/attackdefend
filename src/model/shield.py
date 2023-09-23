import pygame
from constants import SHIELD_DIAMETER, PLAYER_SIZE
from controller.shield_controller import ShieldController
from view.shield_view import ShieldView


class Shield(pygame.sprite.Sprite):
    def __init__(self, game_model, player, image_manager):
        super().__init__()
        self.game_model = game_model
        self.player = player
        self.image_manager = image_manager

        self.x = 0
        self.y = 0
        self.diameter = SHIELD_DIAMETER

        self.screen = pygame.display.get_surface()
        self.image = image_manager.get_image('shield1')
        self.surf = pygame.Surface((SHIELD_DIAMETER, SHIELD_DIAMETER), pygame.SRCALPHA)
        self.rect = self.surf.get_rect()

        self.view = ShieldView(self)
        self.controller = ShieldController(self, self.view)

    def update_image(self):
        shield_level = self.player.attributes_bought.get('shield', 0)
        if shield_level > 0:
            image = self.image_manager.get_specific_shield_image(shield_level)
            self.image = pygame.transform.scale(image, (self.diameter, self.diameter))
        else:
            self.image = None

    def update_diameter_and_surface(self):
        player_diameter = self.player.rect.width
        self.diameter = int(SHIELD_DIAMETER * (player_diameter / PLAYER_SIZE))
        self.surf = pygame.Surface((self.diameter, self.diameter), pygame.SRCALPHA)
        self.rect = self.surf.get_rect()
        self.update_image()

    def update(self):
        self.surf.fill((0, 0, 0, 0))
        self.update_image()
        self.controller.update()
