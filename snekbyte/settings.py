# Board Dimensions
BOARD_WIDTH = 40
BOARD_HEIGHT = 20

# Game Characters
SNAKE_HEAD_CHAR = "@"
SNAKE_BODY_CHAR = "o"
FOOD_CHAR = "*"
OBSTACLE_CHAR = "#"
WALL_CHAR = "#"

# Game Mechanics
INITIAL_SNAKE_LENGTH = 3
INITIAL_SNAKE_POSITION = [(BOARD_WIDTH // 2, BOARD_HEIGHT // 2)]
BASE_SPEED = 0.2  # Initial seconds per game tick
SPEED_INCREMENT_FACTOR = 0.9 # Speed multiplier on food eaten
MIN_SPEED = 0.05 # Maximum speed

# WonQ Mode Specifics
WONQ_MODE_OBSTACLE_COUNT = 5