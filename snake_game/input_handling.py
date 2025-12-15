import pygame
from typing import Any
from .core import Direction

def handle_input() -> Any:
    """
    Handles user input for controlling the snake and game speed.

    Returns:
        - Direction: If an arrow key is pressed.
        - "QUIT": If the game should be terminated.
        - ('speed', delta): If the speed should be changed.
        - None: If there is no relevant input.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "QUIT"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "QUIT"
            # Directions
            elif event.key == pygame.K_UP:
                return Direction.UP
            elif event.key == pygame.K_DOWN:
                return Direction.DOWN
            elif event.key == pygame.K_LEFT:
                return Direction.LEFT
            elif event.key == pygame.K_RIGHT:
                return Direction.RIGHT
            # Speed control
            elif event.key == pygame.K_COMMA: # <
                return ('speed', -1)
            elif event.key == pygame.K_PERIOD: # >
                return ('speed', 1)
    return None # No relevant input

def handle_game_over_input() -> str | None:
    """
    Handles input for the game over menu.

    Returns:
        - "SWITCH": To switch between menu options.
        - "SELECT": To select the current option.
        - "QUIT": To quit the game.
        - None: If there is no relevant input.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "QUIT"
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "QUIT"
            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                return "SWITCH"
            elif event.key == pygame.K_RETURN:
                return "SELECT"
    return None