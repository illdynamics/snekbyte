import curses
from typing import Any
from .game_logic import GameState, GameStatus
from .utils.constants import (
    BOARD_HEIGHT,
    BOARD_WIDTH,
    FOOD_CHAR,
    OBSTACLE_CHAR,
    SNAKE_BODY_CHAR,
    SNAKE_HEAD_CHAR,
    WALL_CHAR,
)

def initialize_screen() -> Any:
    """
    Initializes the curses screen.

    Returns:
        curses.WindowObject: The main window object.
    """
    stdscr = curses.initscr()
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
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
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            if y == 0 or y == BOARD_HEIGHT - 1 or x == 0 or x == BOARD_WIDTH - 1:
                try:
                    stdscr.addch(y, x, WALL_CHAR)
                except curses.error:
                    pass

def draw_snake(stdscr: Any, snake: list[tuple[int, int]]) -> None:
    """
    Draws the snake on the screen.

    Args:
        stdscr (curses.WindowObject): The main window object.
        snake (list[tuple[int, int]]): A list of coordinates for the snake's segments.
    """
    if not snake:
        return
    try:
        head_y, head_x = snake[0]
        stdscr.addch(head_y, head_x, SNAKE_HEAD_CHAR)
        for segment in snake[1:]:
            seg_y, seg_x = segment
            stdscr.addch(seg_y, seg_x, SNAKE_BODY_CHAR)
    except curses.error:
        pass

def draw_food(stdscr: Any, food: tuple[int, int]) -> None:
    """
    Draws the food on the screen.

    Args:
        stdscr (curses.WindowObject): The main window object.
        food (tuple[int, int]): The coordinates of the food.
    """
    try:
        food_y, food_x = food
        stdscr.addch(food_y, food_x, FOOD_CHAR)
    except curses.error:
        pass

def draw_obstacles(stdscr: Any, obstacles: list[tuple[int, int]]) -> None:
    """
    Draws the persistent obstacles in WonQ mode.

    Args:
        stdscr (curses.WindowObject): The main window object.
        obstacles (list[tuple[int, int]]): A list of coordinates for the obstacles.
    """
    for obs_y, obs_x in obstacles:
        try:
            stdscr.addch(obs_y, obs_x, OBSTACLE_CHAR)
        except curses.error:
            pass

def draw_info_bar(stdscr: Any, game_state: GameState) -> None:
    """
    Draws the information bar at the top of the screen (score, etc.).

    Args:
        stdscr (curses.WindowObject): The main window object.
        game_state (GameState): The current state of the game.
    """
    score_text = f"Score: {game_state.score}"
    info_text = score_text
    if game_state.wonq_mode:
        info_text += f" | WonQ Mode Active | Shit Counter: {game_state.shit_counter}/5"
    
    try:
        stdscr.addstr(BOARD_HEIGHT, 0, info_text.ljust(BOARD_WIDTH - 1))
    except curses.error:
        pass

def draw_game_over(stdscr: Any, score: int) -> None:
    """
    Displays the game over screen.

    Args:
        stdscr (curses.WindowObject): The main window object.
        score (int): The player's final score.
    """
    h, w = stdscr.getmaxyx()
    msg = f"GAME OVER! Final Score: {score}. Press 'q' to quit."
    x = w // 2 - len(msg) // 2
    y = h // 2
    try:
        stdscr.addstr(y, x, msg)
        stdscr.refresh()
    except curses.error:
        pass

def draw_splash_screen(stdscr: Any) -> None:
    """
    Displays the WonQ mode splash screen with ASCII art.

    Args:
        stdscr (curses.WindowObject): The main window object.
    """
    h, w = stdscr.getmaxyx()
    splash_text = "Welcome to WonQ Mode. Press any key to start..."
    x = w // 2 - len(splash_text) // 2
    y = h // 2
    try:
        stdscr.addstr(y, x, splash_text)
        stdscr.refresh()
        stdscr.getch()
    except curses.error:
        pass

def cleanup_screen(stdscr: Any) -> None:
    """
    Cleans up the curses screen before exiting.

    Args:
        stdscr (curses.WindowObject): The main window object.
    """
    stdscr.keypad(False)
    curses.nocbreak()
    curses.echo()
    curses.endwin()