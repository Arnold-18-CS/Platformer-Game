import pygame

from modules.object import Object
from modules.utils import load_sprite_sheets


class Fire(Object):
    """
    Contains the description of the fire objects
    """

    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["on"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))

    def on(self):
        """
        Function to set the fire to be on
        """
        self.animation_name = "on"

    def off(self):
        """
        Function to set the fire to off
        """
        self.animation_name = "off"

    def loop(self):
        """
        Looping function to maintain fire object
        """
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0
