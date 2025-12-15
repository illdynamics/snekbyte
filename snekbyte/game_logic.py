import random
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Tuple
from .utils.constants import (
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
    RUNNING = auto()
    GAME_OVER = auto()
    PAUSED = auto()

@dataclass
class GameState:
    """Dataclass to hold the entire state of the game."""
    snake: List[Tuple[int, int]] = field(default_factory=list)
    food: Tuple[int, int] = (0, 0)
    direction: Direction = Direction.RIGHT
    score: int = 0
    status: GameStatus = GameStatus.RUNNING
    wonq_mode: bool = False
    obstacles: List[Tuple[int, int]] = field(default_factory=list)
    shit_counter: int = 0

def initialize_game(wonq_mode: bool = False) -> GameState:
    """
    Initializes the game state for a new game.

    Args:
        wonq_mode (bool): Flag to enable or disable WonQ mode.

    Returns:
        GameState: A new GameState object.
    """
    y, x = INITIAL_SNAKE_POSITION
    snake = [(y, x - i) for i in range(INITIAL_SNAKE_LENGTH)]
    
    state = GameState(snake=snake, wonq_mode=wonq_mode)
    state.food = _generate_food(state)
    return state

def _generate_food(game_state: GameState) -> Tuple[int, int]:
    """
    Generates a new food item at a random position, not on the snake or obstacles.

    Args:
        game_state (GameState): The current state of the game.

    Returns:
        Tuple[int, int]: The coordinates of the new food item.
    """
    occupied_positions = set(game_state.snake) | set(game_state.obstacles)
    while True:
        food_pos = (random.randint(1, BOARD_HEIGHT - 2), random.randint(1, BOARD_WIDTH - 2))
        if food_pos not in occupied_positions:
            return food_pos

def update_game_state(game_state: GameState) -> GameState:
    """
    Updates the game state for the next frame, including snake movement and food collision.

    Args:
        game_state (GameState): The current state of the game.

    Returns:
        GameState: The updated game state.
    """
    if game_state.status != GameStatus.RUNNING:
        return game_state

    head_y, head_x = game_state.snake[0]
    
    if game_state.direction == Direction.UP:
        new_head = (head_y - 1, head_x)
    elif game_state.direction == Direction.DOWN:
        new_head = (head_y + 1, head_x)
    elif game_state.direction == Direction.LEFT:
        new_head = (head_y, head_x - 1)
    else:  # Direction.RIGHT
        new_head = (head_y, head_x + 1)
    
    game_state.snake.insert(0, new_head)

    if new_head == game_state.food:
        game_state.score += 1
        if game_state.wonq_mode:
            game_state.shit_counter += 1
            if game_state.shit_counter >= 5:
                game_state.shit_counter = 0
                game_state.obstacles.append(game_state.snake[-1])

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
    head_y, head_x = game_state.snake[0]

    if not (0 < head_y < BOARD_HEIGHT - 1 and 0 < head_x < BOARD_WIDTH - 1):
        game_state.status = GameStatus.GAME_OVER
        return game_state

    if (head_y, head_x) in game_state.snake[1:]:
        game_state.status = GameStatus.GAME_OVER
        return game_state
        
    if (head_y, head_x) in game_state.obstacles:
        game_state.status = GameStatus.GAME_OVER
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
    current_direction = game_state.direction
    if (new_direction == Direction.UP and current_direction != Direction.DOWN) or \
       (new_direction == Direction.DOWN and current_direction != Direction.UP) or \
       (new_direction == Direction.LEFT and current_direction != Direction.RIGHT) or \
       (new_direction == Direction.RIGHT and current_direction != Direction.LEFT):
        game_state.direction = new_direction
    return game_state