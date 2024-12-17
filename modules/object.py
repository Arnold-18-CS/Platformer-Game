import pygame
from modules.utils import get_block, get_block2

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        
class CongratulationsBlock(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)  # Initialize the object at the given position
        block = get_block2(size)  # Get the block image using get_block2
        self.image.blit(block, (0, 0))  # Blit the block image onto the object surface
        self.mask = pygame.mask.from_surface(self.image)