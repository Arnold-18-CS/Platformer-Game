import pygame

from modules.asset_manager import AssetManager
from modules.constants import GRAVITY, JUMP_VEL


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    ANIMATION_DELAY = 40

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.SPRITES = AssetManager.load_sprites(
            "MainCharacters", "MaskDude", 32, 32, True
        )
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
        self.last_update = pygame.time.get_ticks()  # Tracks the last sprite update

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

    def apply_gravity(self, fps):
        """Applies gravity to the player."""
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.fall_count += 1  # Tracks how long the player has been falling

    def handle_movement(self):
        """Updates the player's position based on velocities."""
        self.move(self.x_vel, self.y_vel)

    def handle_hits(self, fps):
        """Handles hit logic and resets the hit status after a certain duration."""
        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:  # Hit lasts for 2 seconds
            self.hit = False
            self.hit_count = 0

    def update_sprite(self):
        """Updates the sprite based on player state and time."""
        # Define the animation state dictionary
        animation_state = {
            "hit": "hit",
            "jump": "jump" if self.jump_count == 1 else "double_jump",
            "fall": "fall" if self.y_vel > self.GRAVITY * 2 else "idle",
            "run": "run" if self.x_vel != 0 else "idle",
        }

        # Determine the sprite sheet based on player state
        sprite_sheet = animation_state.get(
            "hit"
            if self.hit
            else (
                "jump"
                if self.y_vel < 0
                else "fall" if self.y_vel > self.GRAVITY * 2 else "run"
            )
        )

        sprite_sheet_name = f"{sprite_sheet}_{self.direction}"
        sprites = self.SPRITES[sprite_sheet_name]  # Load the correct sprite sheet

        # # Use time-based animation to update the animation frame
        current_time = pygame.time.get_ticks()
        # Control the animation speed
        if current_time - self.last_update >= self.ANIMATION_DELAY:
            self.last_update = current_time  # Update the last update time
            self.animation_count += 1  # Increment the animation frame index

        # Set the current sprite
        self.sprite = sprites[self.animation_count % len(sprites)]
        # self.animation_count += 1

        # Update rect and mask to reflect new sprite size/position
        self.update()

    def loop(self, fps):
        """Main loop to update player state."""
        self.apply_gravity(fps)
        self.handle_movement()
        self.handle_hits(fps)
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.y_vel = 0  # Set y velocity to 0 to stop upward movement
        self.jump_count = 0  # Reset jump count if needed

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))
