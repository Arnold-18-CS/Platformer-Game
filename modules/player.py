import pygame
from modules.utils import load_sprite_sheets
from modules.constants import JUMP_VEL, GRAVITY
from modules.asset_manager import AssetManager


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.SPRITES = AssetManager.load_sprites("MainCharacters", "MaskDude",32,32,True)
        self.sprite = self.SPRITES["idle_left"][0]  # Default sprite
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.JUMP_VEL = JUMP_VEL
        self.GRAVITY = GRAVITY
        self.hit = False
        self.hit_count = 0

    def jump(self):
        self.y_vel = -self.JUMP_VEL
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.y_vel = 0  # Set y velocity to 0 to stop upward movement
        self.jump_count = 0  # Reset jump count if needed


    def update_sprite(self):
        animation_state = {
            "hit": "hit",
            "jump": "jump" if self.jump_count == 1 else "double_jump",
            "fall": "fall" if self.y_vel > self.GRAVITY * 2 else "idle",
            "run": "run" if self.x_vel != 0 else "idle"
        }

        sprite_sheet = animation_state.get(
            "hit" if self.hit else 
            "jump" if self.y_vel < 0 else 
            "fall" if self.y_vel > self.GRAVITY * 2 else
            "run")

        sprite_sheet_name = f"{sprite_sheet}_{self.direction}"
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1


    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

