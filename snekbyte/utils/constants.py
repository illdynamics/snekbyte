import pygame

# -- Pygame Specific Constants (for snekbyte.py App Menu) --

# Screen Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 155, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (40, 40, 40)
YELLOW = (255, 255, 0)
LIGHT_GRAY = (200, 200, 200)
BACKGROUND_COLOR = BLACK

# Font Settings
FONT_NAME = None
FONT_SIZE_LARGE = 72
FONT_SIZE_MEDIUM = 50
FONT_SIZE_SMALL = 36

# Menu Texts
TITLE_TEXT = "SnekByte"
START_GAME_TEXT = "Start Pygame Game"
SETTINGS_TEXT = "Settings"
QUIT_TEXT = "Quit"

# Settings Menu Texts
BACK_TEXT = "Back"


# -- Curses Specific Constants (Not used by the Pygame App Menu) --

# Board Dimensions
BOARD_WIDTH = 40
BOARD_HEIGHT = 20

# Game Characters
SNAKE_HEAD_CHAR = "@"
SNAKE_BODY_CHAR = "o"
FOOD_CHAR = "*"
OBSTACLE_CHAR = "#"
WALL_CHAR = "#"

# Initial Game Settings
INITIAL_SNAKE_LENGTH = 3
INITIAL_SNAKE_POSITION = (BOARD_HEIGHT // 2, BOARD_WIDTH // 2)