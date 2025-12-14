"""
Centralized configuration file for the Snake game.

This file contains all the core settings for the game, including screen dimensions,
colors, frame rate, and game-specific constants.
"""

# Game Window Settings
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FPS = 15

# For compatibility with existing skeletons that might use SCREEN_*
SCREEN_WIDTH = WINDOW_WIDTH
SCREEN_HEIGHT = WINDOW_HEIGHT

# Grid Settings
BLOCK_SIZE = 20

# Ensure window dimensions are multiples of block size for a perfect grid
assert WINDOW_WIDTH % BLOCK_SIZE == 0, "Window width must be a multiple of block size."
assert WINDOW_HEIGHT % BLOCK_SIZE == 0, "Window height must be a multiple of block size."

# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Font Settings
FONT_SIZE = 25
# Using None for pygame's default font. A specific font file can be used here.
FONT_NAME = None

# Directions Tuples - while core.py uses an Enum, some modules might expect these.
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)