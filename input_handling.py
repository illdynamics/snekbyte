import pygame
import sys
from typing import Dict, Any, Tuple
from settings import UP, DOWN, LEFT, RIGHT

def handle_input(game_state: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
    """
    Handles user input for controlling the snake and quitting the game.

    Args:
        game_state (Dict[str, Any]): The current state of the game.

    Returns:
        Tuple[Dict[str, Any], bool]: The potentially updated game state and a boolean
                                     indicating if the game should quit.
    """
    should_quit = False
    current_direction = game_state.get('direction', RIGHT)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            should_quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and current_direction != DOWN:
                game_state['direction'] = UP
            elif event.key == pygame.K_DOWN and current_direction != UP:
                game_state['direction'] = DOWN
            elif event.key == pygame.K_LEFT and current_direction != RIGHT:
                game_state['direction'] = LEFT
            elif event.key == pygame.K_RIGHT and current_direction != LEFT:
                game_state['direction'] = RIGHT

    return game_state, should_quit