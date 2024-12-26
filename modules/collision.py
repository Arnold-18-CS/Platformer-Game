import pygame

from modules.constants import HEIGHT, PLAYER_VEL


def collide(player, objects, dx):
    """
    Check for horizontal collision between the player and objects.

    Moves the player by a given delta (`dx`) and checks for collisions with objects.
    Then resets the player's position to its original state.

    :param player: The player object (with rect and move methods).
    :param objects: List of game objects to check for collisions.
    :param dx: Horizontal movement delta for the collision check.
    :return: The first object collided with, or None if no collision occurred.
    """
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_vertical_collision(player, objects, dy):
    """
    Handle vertical collisions for the player.

    Adjusts the player's position if a collision occurs during vertical movement,
    ensuring the player lands or hits their head correctly.

    :param player: The player object (with rect and movement methods).
    :param objects: List of game objects to check for collisions.
    :param dy: Vertical movement delta for the collision check.
    :return: A list of all objects the player collided with vertically.
    """
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def handle_move(player, objects):
    """
    Handle player movement and collisions.

    Processes user input to move the player horizontally and checks for collisions
    on both horizontal and vertical axes. Also detects interactions with fire objects.

    :param player: The player object (with movement and collision methods).
    :param objects: List of game objects to check for collisions.
    """
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()


def check_spike_collision(player, spikes, block_size):
    """
    Check for collisions between the player and spikes.

    If the player collides with a spike, their position is reset.

    :param player: The player object (with a rect attribute).
    :param spikes: List of spike objects to check for collisions.
    :param block_size: The size of a block (used to calculate reset position).
    :return: True if a collision occurred, False otherwise.
    """
    for spike in spikes:
        if player.rect.colliderect(spike.rect):  # If player touches the spike
            print("Ouch! You hit a spike!")
            player.rect.x = (
                100  # Reset player position as an example (or reduce health)
            )
            player.rect.y = HEIGHT - block_size - 50
            return True
    return False


def check_congratulation_collision(player, congrat_block):
    """
    Check if the player has reached the congratulation block.

    First performs a pixel-perfect collision check using masks, followed by a bounding box check.

    :param player: The player object (with rect and mask attributes).
    :param congrat_block: The congratulation block to check for collisions.
    :return: True if the player has collided with the block, False otherwise.
    """
    # First, check for pixel-perfect collision using the mask (more precise)
    if pygame.sprite.collide_mask(player, congrat_block):
        print("Congratulations! You've reached the special block!")
        return True

    # Check if the player's rectangle collides with the block's rectangle (bounding box check)
    if player.rect.colliderect(congrat_block.rect):
        print("Congratulations! You've reached the special block!")
        return True

    return False
