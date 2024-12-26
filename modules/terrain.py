"""
Module handles terrain generations
"""

import random

from modules.object import Block, CongratulationsBlock


def create_random_terrain(block_size, width, height):
    """Terrain generation."""
    terrain = []
    max_platforms = 20  # Total number of platforms
    platform_width = width // block_size  # How many blocks fit horizontally

    # Create the base floor
    for i in range(-platform_width, platform_width * 2):
        terrain.append(Block(i * block_size, height - block_size, block_size))

    last_x = 0  # Start placing platforms from the beginning
    platform_y = height - block_size  # Start the first platform at the floor level

    # Generate multiple layers of platforms
    for _ in range(max_platforms):
        gap = random.randint(1, 3) * block_size  # Randomize the gap between platforms
        platform_x = last_x + gap

        # Randomize platform height (ensure there are multiple layers within jumping range)
        platform_y = (
            height - block_size - random.randint(2, 6) * block_size
        )  # Multiple layers

        # Create a platform of random length
        platform_length = random.randint(3, 7)
        for i in range(platform_length):
            terrain.append(Block(platform_x + i * block_size, platform_y, block_size))

        last_x = platform_x + platform_length * block_size  # Update last X position

    return terrain


def create_random_target_block(
    block_size, width, height, player_pos, objects, max_attempts=50
):
    """
    Create a random target block, ensuring it's far enough from the player
    and does not collide with existing objects.

    Parameters:
    - block_size: Size of the block (width and height).
    - width, height: Dimensions of the game screen.
    - player_pos: Tuple representing the player's current (x, y) position.
    - objects: List of existing game objects to avoid collisions.
    - max_attempts: Maximum number of tries to find a valid position.

    Returns:
    - A valid CongratulationsBlock instance.
    """
    min_x = player_pos[0] + 50  # Ensure the block is far enough horizontally
    max_x = width - 100  # Leave space from the right edge

    for _ in range(max_attempts):  # Retry up to max_attempts
        # Clamp values to ensure valid range
        if min_x >= max_x:
            min_x = max_x - 1

        x_position = random.randint(min_x, max_x)
        y_position = random.randint(0, height - block_size)

        # Create the target block
        target_block = CongratulationsBlock(x_position, y_position, block_size)

        # Check for collisions with existing objects
        if not any(target_block.rect.colliderect(obj.rect) for obj in objects):
            return target_block

    # If a valid position is not found after max_attempts
    raise ValueError(
        "Could not find a valid position for the target block after multiple attempts."
    )
