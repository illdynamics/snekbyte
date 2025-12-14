import pygame
import sys
from typing import Tuple

from .core import Direction

def handle_input(current_direction: Direction) -> Tuple[Direction, bool]:
    """
    Handles user input for controlling the snake and quitting the game.
    This function processes the event queue from pygame.

    The contract for this function is to:
    - Return the new direction for the snake.
    - Return a boolean flag indicating if the game should be terminated.

    Args:
        current_direction (Direction): The current direction of the snake.

    Returns:
        Tuple[Direction, bool]: A tuple containing the new direction and a boolean
                                indicating if the game should quit.
    """
    new_direction = current_direction
    quit_flag = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_flag = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit_flag = True
            # The game logic in core.Snake.change_direction prevents
            # the snake from reversing, so we just pass the new direction intent.
            elif event.key == pygame.K_UP:
                new_direction = Direction.UP
            elif event.key == pygame.K_DOWN:
                new_direction = Direction.DOWN
            elif event.key == pygame.K_LEFT:
                new_direction = Direction.LEFT
            elif event.key == pygame.K_RIGHT:
                new_direction = Direction.RIGHT

    return new_direction, quit_flag