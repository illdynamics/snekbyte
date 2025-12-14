import pygame
from typing import Dict, Any, Tuple
from .config import UP, DOWN, LEFT, RIGHT

def handle_input(game_state: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
    """
    Handles user input for controlling the snake and quitting the game.

    Args:
        game_state (Dict[str, Any]): The current state of the game.

    Returns:
        Tuple[Dict[str, Any], bool]: The potentially updated game state and a boolean
                                     indicating if the game should quit.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return game_state, True
        if event.type == pygame.KEYDOWN:
            current_direction = game_state["snake_direction"]
            if event.key == pygame.K_UP and current_direction != DOWN:
                game_state["snake_direction"] = UP
            elif event.key == pygame.K_DOWN and current_direction != UP:
                game_state["snake_direction"] = DOWN
            elif event.key == pygame.K_LEFT and current_direction != RIGHT:
                game_state["snake_direction"] = LEFT
            elif event.key == pygame.K_RIGHT and current_direction != LEFT:
                game_state["snake_direction"] = RIGHT
    return game_state, False