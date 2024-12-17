import pygame
from modules.constants import *


pygame.init()
pygame.display.set_caption(GAME_NAME)

window = pygame.display.set_mode((WIDTH, HEIGHT))

from modules.player import Player
from modules.fire import Fire
from modules.terrain import create_random_terrain, create_random_target_block
from modules.utils import get_background
from modules.collision import handle_move, check_congratulation_collision

def draw(window, background, bg_image, player, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)

    pygame.display.update()
    
# Initialize the game
def main(window):
    clock = pygame.time.Clock()
    FPS = 60

    # Load background
    background, bg_image = get_background("Blue.png")
    block_size = 96

    # Create player object
    player = Player(100, 100, 50, 50)

    # Create the fire object
    fire = Fire(100, HEIGHT - block_size - 64, 16, 32)
    fire.on()

    # Create terrain
    objects = create_random_terrain(block_size, WIDTH, HEIGHT)
    objects.append(fire)

    # Create target block safely
    target_block = None
    try:
        target_block = create_random_target_block(block_size, WIDTH, HEIGHT, player.rect.topleft, objects)
        objects.append(target_block)
    except ValueError as e:
        print(f"Error creating target block: {e}")

    offset_x = 0
    scroll_area_width = 200

    # Main loop
    run = True
    while run:
        clock.tick(FPS)  # Cap the frame rate

        # --- Event Handling ---
        run = handle_events(player)

        # --- Update Logic ---
        player.loop(FPS)
        fire.loop()
        handle_move(player, objects)

        # Check for target block collision
        if target_block and check_congratulation_collision(player, target_block):
            display_congratulations(window)

        # --- Camera Logic ---
        offset_x = handle_scrolling(player)

        # --- Draw Everything ---
        draw_frame(window, background, bg_image, player, objects, offset_x)

    # Clean up
    pygame.quit()


# Event handling
def handle_events(player):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.jump_count < 2:
                player.jump()
    return True


# Handle camera scrolling
def handle_scrolling(player):
    # if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or \
    #    ((player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
    #     offset_x += player.x_vel
        
    """
    Calculate offset to center the camera on the player.
    """
    offset_x = player.rect.centerx - WIDTH // 2
    return offset_x


# Draw all game elements
def draw_frame(window, background, bg_image, player, objects, offset_x):
    """Draw all game elements"""
    window.fill((0, 0, 0))  # Clear the screen
    draw(window, background, bg_image, player, objects, offset_x)  # Player is drawn here
    pygame.display.update()
  
def display_congratulations(window):
    """Show the congratulatory message and reload the game after 3 seconds"""
    font = pygame.font.SysFont('Serif', 50)
    text = font.render("Congratulations! You've won!", True, (255, 255, 255))
    window.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()

    pygame.time.wait(3000)  # Wait for 3 seconds
    reload_game()  # Reload the game or restart the level

def reload_game():
    """Function to reload or restart the game"""
    # You can either reset the level or restart the entire game by reinitializing the main function
    main(window)

if __name__ == "__main__":
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    main(window)
