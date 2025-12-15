import curses
from typing import Any

from .game_logic import GameState, GameStatus
from .settings import (
    BOARD_HEIGHT,
    BOARD_WIDTH,
    FOOD_CHAR,
    OBSTACLE_CHAR,
    SNAKE_BODY_CHAR,
    SNAKE_HEAD_CHAR,
    WALL_CHAR,
)

SMILEY_TURD_ART = [
    "      .--.    ",
    "     /  ..\\   ",
    "    /  <  /   ",
    "   /   /  \\   ",
    "  /   /`---'  ",
    "_/__.'        ",
]

def initialize_screen() -> Any:
    """
    Initializes the curses screen.

    Returns:
        curses.WindowObject: The main window object.
    """
    stdscr = curses.initscr()
    curses.curs_set(0)
    curses.noecho()
    stdscr.keypad(True)
    stdscr.nodelay(True)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Food
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Score/Wall
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)    # Game Over / Obstacle
    return stdscr

def draw_game(stdscr: Any, game_state: GameState) -> None:
    """
    Draws the entire game screen, including walls, snake, food, and info bar.

    Args:
        stdscr (curses.WindowObject): The main window object.
        game_state (GameState): The current state of the game.
    """
    stdscr.clear()
    draw_walls(stdscr)
    draw_snake(stdscr, game_state.snake)
    draw_food(stdscr, game_state.food)
    if game_state.wonq_mode:
        draw_obstacles(stdscr, game_state.obstacles)
    draw_info_bar(stdscr, game_state)
    stdscr.refresh()

def draw_walls(stdscr: Any) -> None:
    """
    Draws the border walls of the game board.

    Args:
        stdscr (curses.WindowObject): The main window object.
    """
    wall_color = curses.color_pair(3)
    for y in range(BOARD_HEIGHT):
        stdscr.addstr(y, 0, WALL_CHAR, wall_color)
        stdscr.addstr(y, BOARD_WIDTH - 1, WALL_CHAR, wall_color)
    for x in range(BOARD_WIDTH):
        stdscr.addstr(0, x, WALL_CHAR, wall_color)
        stdscr.addstr(BOARD_HEIGHT - 1, x, WALL_CHAR, wall_color)

def draw_snake(stdscr: Any, snake: list[tuple[int, int]]) -> None:
    """
    Draws the snake on the screen.

    Args:
        stdscr (curses.WindowObject): The main window object.
        snake (list[tuple[int, int]]): A list of coordinates for the snake's segments.
    """
    snake_color = curses.color_pair(1)
    stdscr.addstr(snake[0][0], snake[0][1], SNAKE_HEAD_CHAR, snake_color)
    for segment in snake[1:]:
        stdscr.addstr(segment[0], segment[1], SNAKE_BODY_CHAR, snake_color)

def draw_food(stdscr: Any, food: tuple[int, int]) -> None:
    """
    Draws the food on the screen.

    Args:
        stdscr (curses.WindowObject): The main window object.
        food (tuple[int, int]): The coordinates of the food.
    """
    food_color = curses.color_pair(2)
    stdscr.addstr(food[0], food[1], FOOD_CHAR, food_color)

def draw_obstacles(stdscr: Any, obstacles: list[tuple[int, int]]) -> None:
    """
    Draws the persistent obstacles in WonQ mode.

    Args:
        stdscr (curses.WindowObject): The main window object.
        obstacles (list[tuple[int, int]]): A list of coordinates for the obstacles.
    """
    obstacle_color = curses.color_pair(4)
    for pos in obstacles:
        stdscr.addstr(pos[0], pos[1], OBSTACLE_CHAR, obstacle_color)

def draw_info_bar(stdscr: Any, game_state: GameState) -> None:
    """
    Draws the information bar at the top of the screen (score, etc.).

    Args:
        stdscr (curses.WindowObject): The main window object.
        game_state (GameState): The current state of the game.
    """
    score_text = f"Score: {game_state.score}"
    if game_state.wonq_mode:
        wonq_text = f" (WONQ!) Shitcounter: {game_state.shitcounter}"
        info_text = score_text + wonq_text
    else:
        info_text = score_text
    
    stdscr.addstr(0, 2, info_text, curses.color_pair(3))

def draw_game_over(stdscr: Any, score: int) -> None:
    """
    Displays the game over screen.

    Args:
        stdscr (curses.WindowObject): The main window object.
        score (int): The player's final score.
    """
    h, w = stdscr.getmaxyx()
    game_over_text = "GAME OVER"
    score_text = f"Final Score: {score}"
    retry_text = "Press 'r' to Retry or 'q' to Quit"
    
    stdscr.addstr(h // 2 - 2, (w - len(game_over_text)) // 2, game_over_text, curses.color_pair(4))
    stdscr.addstr(h // 2, (w - len(score_text)) // 2, score_text, curses.color_pair(3))
    stdscr.addstr(h // 2 + 2, (w - len(retry_text)) // 2, retry_text, curses.color_pair(3))
    stdscr.refresh()

def draw_splash_screen(stdscr: Any) -> None:
    """
    Displays the WonQ mode splash screen with ASCII art.

    Args:
        stdscr (curses.WindowObject): The main window object.
    """
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    art_height = len(SMILEY_TURD_ART)
    art_width = len(SMILEY_TURD_ART[0])
    
    start_y = h // 2 - art_height // 2 - 2
    start_x = w // 2 - art_width // 2

    for i, line in enumerate(SMILEY_TURD_ART):
        stdscr.addstr(start_y + i, start_x, line, curses.color_pair(2))
        
    continue_text = "Press any key to continue..."
    stdscr.addstr(start_y + art_height + 2, (w - len(continue_text)) // 2, continue_text, curses.color_pair(3))
    stdscr.refresh()

def cleanup_screen(stdscr: Any) -> None:
    """
    Cleans up the curses screen before exiting.

    Args:
        stdscr (curses.WindowObject): The main window object.
    """
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()