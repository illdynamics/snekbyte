import sys
import pygame
from typing import Dict, Any

from snake_game.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLOCK_SIZE
from snake_game.core import GameState, Direction
from snake_game.rendering import initialize_screen, draw_game, display_game_over
from snake_game.input_handling import handle_input

def adapt_game_state_for_rendering(game_state: GameState) -> Dict[str, Any]:
    """
    Converts the GameState object into a dictionary for the rendering module.

    This adapter function acts as a bridge between the core game logic (which uses
    the GameState class) and the rendering engine (which expects a dictionary with
    Pygame-specific objects). It decouples the game's internal state representation
    from the rendering implementation, allowing either to be changed independently.
    Specifically, it converts the logical coordinates (Points) from the game state
    into pygame.Rect objects required for drawing on the screen.

    Args:
        game_state (GameState): The current state of the game object.

    Returns:
        Dict[str, Any]: A dictionary containing 'snake_body', 'food_pos', and 'score'
                        in a format suitable for the rendering.draw_game function.
    """
    # Convert the list of Point objects for the snake's body into a list of pygame.Rect objects.
    snake_body_rects = [
        pygame.Rect(p.x, p.y, BLOCK_SIZE, BLOCK_SIZE)
        for p in game_state.snake.body
    ]
    
    # Convert the Point object for the food's position into a pygame.Rect object.
    food_pos_rect = pygame.Rect(
        game_state.food.position.x, game_state.food.position.y, BLOCK_SIZE, BLOCK_SIZE
    )

    # The score is already in the correct format (integer).
    return {
        'snake_body': snake_body_rects,
        'food_pos': food_pos_rect,
        'score': game_state.score,
    }

def main():
    """
    Initializes the game, runs the main game loop, and quits the game.
    """
    pygame.init()
    screen = initialize_screen()
    clock = pygame.time.Clock()

    game_state = GameState(SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE)

    running = True
    while running:
        # 1. Handle Input
        # Assumes the refactored interface from the previous task where handle_input
        # processes the event queue and returns an optional Direction or None to quit.
        new_direction = handle_input()
        if new_direction is None:
            running = False
            continue
        
        game_state.snake.change_direction(new_direction)

        # 2. Update Game State
        game_state.update()

        # 3. Render the screen
        if game_state.is_game_over():
            running = False
        else:
            # Use the adapter to convert the GameState object into a
            # rendering-friendly dictionary before drawing.
            render_data = adapt_game_state_for_rendering(game_state)
            draw_game(screen, render_data)

        pygame.display.flip()
        clock.tick(FPS)

    # After the main loop, display the game over screen with the final score
    display_game_over(screen, game_state.score)
    pygame.display.flip()
    pygame.time.wait(2000)  # Wait for 2 seconds before closing

    pygame.quit()
    sys.exit()