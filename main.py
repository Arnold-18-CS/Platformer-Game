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
from modules.asset_manager import AssetManager

def draw(window, background, bg_image, player, objects, offset_x):
    """Draws the game elements on the window"""
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)

    pygame.display.update()
  
def main(window):
    """Main game function"""
    clock = pygame.time.Clock()
    FPS = 60

    game_should_restart = True  # Add restart flag
    while game_should_restart:
        game_should_restart = False  # Reset the flag for the current session

        # --- Initialize the game state ---
        background, bg_image = get_background("Blue.png")
        player = Player(100, 100, 50, 50)
        fire = Fire(100, HEIGHT - BLOCK_SIZE - 64, 16, 32)
        fire.on()
        objects = create_random_terrain(BLOCK_SIZE, WIDTH, HEIGHT)
        objects.append(fire)

        try:
            target_block = create_random_target_block(BLOCK_SIZE, WIDTH, HEIGHT, player.rect.topleft, objects)
            objects.append(target_block)
        except ValueError as e:
            print(f"Error creating target block: {e}")
            target_block = None

        offset_x = 0
        run = True

        # --- Main Game Loop ---
        while run:
            clock.tick(FPS)

            # Event handling
            run = handle_events(player)

            # Update logic
            player.loop(FPS)
            fire.loop()
            handle_move(player, objects)

            # Check for winning condition
            if target_block and check_congratulation_collision(player, target_block):
                display_congratulations(window)
                game_should_restart = True
                run = False  # Exit the current game loop

            # Camera scrolling
            offset_x = handle_scrolling(player)

            # Drawing
            draw_frame(window, background, bg_image, player, objects, offset_x)

    # Quit the game
    pygame.quit()


# Event handling
def handle_events(player):
    """Handles user inputs and events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.jump_count < 2:
                player.jump()
            if event.key == pygame.K_p: # Pause the game
                pause_game()
    return True


# Handle camera scrolling
def handle_scrolling(player): 
    """
    Calculate offset to center the camera on the player.
    """
    offset_x = player.rect.centerx - WIDTH // 2
    return offset_x

# Draw all game elements
def draw_frame(window, background, bg_image, player, objects, offset_x):
    """Draw all game elements on the frame"""
    window.fill((0, 0, 0))  # Clear the screen
    draw(window, background, bg_image, player, objects, offset_x)  # Player is drawn here
    pygame.display.update()
    
def pause_game():
    """Pauses the game until 'p' is pressed again"""
    paused = True
    font = pygame.font.SysFont(FONT, FONT_SIZE)
    text = font.render("Game Paused - Press 'p' to resume", True, WHITE)
    play_button = AssetManager.load_image("assets/Menu/Buttons/Play.png")
    play_button = pygame.transform.scale(play_button, DEFAULT_ICON_SIZE)
    play_button_rect = play_button.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))
    while paused:
        window.blit(
            text,
            (WIDTH//2 - text.get_width()//2,
            HEIGHT//2 - text.get_height()//2
            )
        )
        window.blit(play_button, play_button_rect)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = False
            
  
def display_congratulations(window):
    """Show the congratulatory message and reload the game after 3 seconds"""
    font = pygame.font.SysFont(FONT, 50)
    text = font.render("Congratulations! You've won!", True, WHITE)
    window.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()

    pygame.time.wait(3000)  # Wait for 3 seconds

if __name__ == "__main__":
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    main(window)
