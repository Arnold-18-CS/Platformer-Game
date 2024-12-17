import pygame
from modules.constants import *

def collide(player, objects, dx):
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
    """Check if the player collides with any spike"""
    for spike in spikes:
        if player.rect.colliderect(spike.rect):  # If player touches the spike
            # Handle the collision, e.g., damage or restart
            print("Ouch! You hit a spike!")
            player.rect.x = 100  # Reset player position as an example (or reduce health)
            player.rect.y = HEIGHT - block_size - 50
            return True
    return False

def check_congratulation_collision(player, congrat_block):
    """Check if player touches any part of the congratulation block (bottom, sides, etc.)"""
    
    # First, check for pixel-perfect collision using the mask (more precise)
    if pygame.sprite.collide_mask(player, congrat_block):
        print("Congratulations! You've reached the special block!")
        return True

    # Check if the player's rectangle collides with the block's rectangle (bounding box check)
    if player.rect.colliderect(congrat_block.rect):
        print("Congratulations! You've reached the special block!")
        return True

    return False


