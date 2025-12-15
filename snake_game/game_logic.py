import random
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Tuple

from .settings import (
    BOARD_HEIGHT,
    BOARD_WIDTH,
    INITIAL_SNAKE_LENGTH,
    INITIAL_SNAKE_POSITION,
)

class Direction(Enum):
    """Enumeration for snake movement directions."""
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

class GameStatus(Enum):
    """Enumeration for the current state of the game."""
    PLAYING = auto()
    GAME_OVER = auto()
    PAUSED = auto()
    SPLASH = auto()

@dataclass
class GameState:
    """Dataclass to hold the entire state of the game."""
    snake: List[Tuple[int, int]]
    direction: Direction
    food: Tuple[int, int]
    score: int
    game_status: GameStatus
    wonq_mode: bool = False
    shitcounter: int = 10
    obstacles: List[Tuple[int, int]] = field(default_factory=list)

def initialize_game(wonq_mode: bool = False) -> GameState:
    """
    Initializes the game state for a new game.

    Args:
        wonq_mode (bool): Flag to enable or disable WonQ mode.

    Returns:
        GameState: A new GameState object.
    """
    snake = [
        (
            INITIAL_SNAKE_POSITION[0],
            INITIAL_SNAKE_POSITION[1] - i,
        )
        for i in range(INITIAL_SNAKE_LENGTH)
    ]
    game_state = GameState(
        snake=snake,
        direction=Direction.RIGHT,
        food=(0, 0),
        score=0,
        game_status=GameStatus.PLAYING,
        wonq_mode=wonq_mode
    )
    game_state.food = _generate_food(game_state)
    return game_state

def _generate_food(game_state: GameState) -> Tuple[int, int]:
    """
    Generates a new food item at a random position, not on the snake or obstacles.

    Args:
        game_state (GameState): The current state of the game.

    Returns:
        Tuple[int, int]: The coordinates of the new food item.
    """
    while True:
        food_pos = (random.randint(1, BOARD_HEIGHT - 2), random.randint(1, BOARD_WIDTH - 2))
        if food_pos not in game_state.snake and food_pos not in game_state.obstacles:
            return food_pos

def update_game_state(game_state: GameState) -> GameState:
    """
    Updates the game state for the next frame, including snake movement and food collision.

    Args:
        game_state (GameState): The current state of the game.

    Returns:
        GameState: The updated game state.
    """
    snake_head = game_state.snake[0]
    if game_state.direction == Direction.UP:
        new_head = (snake_head[0] - 1, snake_head[1])
    elif game_state.direction == Direction.DOWN:
        new_head = (snake_head[0] + 1, snake_head[1])
    elif game_state.direction == Direction.LEFT:
        new_head = (snake_head[0], snake_head[1] - 1)
    else:  # RIGHT
        new_head = (snake_head[0], snake_head[1] + 1)

    game_state.snake.insert(0, new_head)

    if new_head == game_state.food:
        game_state.score += 1
        if game_state.wonq_mode:
            if game_state.shitcounter == 1:
                game_state.obstacles.append(game_state.food)
            
            game_state.shitcounter -= 1
            if game_state.shitcounter == 0:
                game_state.game_status = GameStatus.SPLASH
                game_state.shitcounter = 10
        
        game_state.food = _generate_food(game_state)
    else:
        game_state.snake.pop()

    return game_state

def check_collisions(game_state: GameState) -> GameState:
    """
    Checks for game-ending collisions (walls, self, obstacles).

    Args:
        game_state (GameState): The current state of the game.

    Returns:
        GameState: The game state with an updated status if a collision occurred.
    """
    snake_head = game_state.snake[0]
    
    if (
        snake_head[0] in [0, BOARD_HEIGHT - 1] or
        snake_head[1] in [0, BOARD_WIDTH - 1]
    ):
        game_state.game_status = GameStatus.GAME_OVER
        return game_state

    if snake_head in game_state.snake[1:]:
        game_state.game_status = GameStatus.GAME_OVER
        return game_state

    if game_state.wonq_mode and snake_head in game_state.obstacles:
        game_state.game_status = GameStatus.GAME_OVER
        return game_state

    return game_state

def change_direction(game_state: GameState, new_direction: Direction) -> GameState:
    """
    Changes the snake's direction, preventing it from reversing.

    Args:
        game_state (GameState): The current state of the game.
        new_direction (Direction): The desired new direction.

    Returns:
        GameState: The game state with the updated direction.
    """
    if new_direction == Direction.UP and game_state.direction != Direction.DOWN:
        game_state.direction = new_direction
    elif new_direction == Direction.DOWN and game_state.direction != Direction.UP:
        game_state.direction = new_direction
    elif new_direction == Direction.LEFT and game_state.direction != Direction.RIGHT:
        game_state.direction = new_direction
    elif new_direction == Direction.RIGHT and game_state.direction != Direction.LEFT:
        game_state.direction = new_direction
    return game_state