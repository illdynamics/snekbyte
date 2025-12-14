import random
from collections import namedtuple
from enum import Enum

Point = namedtuple('Point', 'x y')

class Direction(Enum):
    """Enumeration for movement directions."""
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

class Snake:
    """Represents the snake in the game."""
    def __init__(self, width: int, height: int, block_size: int):
        """
        Initializes the Snake object.

        Args:
            width (int): The width of the game area.
            height (int): The height of the game area.
            block_size (int): The size of a single snake segment.
        """
        self.width = width
        self.height = height
        self.block_size = block_size
        
        self.head = Point(width // 2, height // 2)
        self.body = [
            self.head,
            Point(self.head.x - block_size, self.head.y),
            Point(self.head.x - (2 * block_size), self.head.y)
        ]
        self.direction = Direction.RIGHT
        self._growing = False

    def move(self) -> None:
        """
        Moves the snake one step in its current direction.

        The snake moves by adding a new head segment in the direction of
        movement and removing the tail segment, unless the snake is growing.
        """
        x, y = self.head

        if self.direction == Direction.UP:
            y -= self.block_size
        elif self.direction == Direction.DOWN:
            y += self.block_size
        elif self.direction == Direction.LEFT:
            x -= self.block_size
        elif self.direction == Direction.RIGHT:
            x += self.block_size

        self.head = Point(x, y)
        self.body.insert(0, self.head)

        if not self._growing:
            self.body.pop()
        else:
            self._growing = False

    def grow(self) -> None:
        """
        Flags the snake to grow on its next move.

        The next time the snake moves, its tail segment will not be removed,
        effectively increasing its length by one.
        """
        self._growing = True

    def change_direction(self, new_direction: Direction) -> None:
        """
        Changes the snake's direction of movement.

        The snake cannot reverse its direction (e.g., from UP to DOWN).

        Args:
            new_direction (Direction): The new direction to move in.
        """
        if new_direction == Direction.UP and self.direction != Direction.DOWN:
            self.direction = new_direction
        elif new_direction == Direction.DOWN and self.direction != Direction.UP:
            self.direction = new_direction
        elif new_direction == Direction.LEFT and self.direction != Direction.RIGHT:
            self.direction = new_direction
        elif new_direction == Direction.RIGHT and self.direction != Direction.LEFT:
            self.direction = new_direction

    def check_collision(self) -> bool:
        """
        Checks if the snake has collided with itself.

        Returns:
            bool: True if the snake's head has collided with its body,
                  False otherwise.
        """
        return self.head in self.body[1:]

class Food:
    """Represents the food that the snake eats."""
    def __init__(self, width: int, height: int, block_size: int, snake_body: list[Point]):
        """
        Initializes the Food object.

        Args:
            width (int): The width of the game area.
            height (int): The height of the game area.
            block_size (int): The size of a single grid block.
            snake_body (list[Point]): The list of points representing the snake's body.
        """
        self.width = width
        self.height = height
        self.block_size = block_size
        self.position = Point(0, 0)
        self.spawn(snake_body)

    def spawn(self, snake_body: list[Point]) -> None:
        """
        Places the food at a new random location on the game grid.

        The new location will not be on any part of the snake's body.

        Args:
            snake_body (list[Point]): The list of points representing the snake's body.
        """
        while True:
            x = random.randint(0, (self.width - self.block_size) // self.block_size) * self.block_size
            y = random.randint(0, (self.height - self.block_size) // self.block_size) * self.block_size
            self.position = Point(x, y)
            if self.position not in snake_body:
                break

class GameState:
    """Manages the overall state of the game."""
    def __init__(self, width: int, height: int, block_size: int):
        """
        Initializes the game state.

        Args:
            width (int): The width of the game window.
            height (int): The height of the game window.
            block_size (int): The size of each grid block (and snake segment).
        """
        self.width = width
        self.height = height
        self.block_size = block_size

        self.snake = Snake(width, height, block_size)
        self.food = Food(width, height, block_size, self.snake.body)
        self.score = 0
        self.game_over = False

    def update(self) -> None:
        """
        Updates the game state for a single frame.

        This method moves the snake, checks for collisions with walls, itself,
        and food, and updates the score and game-over status accordingly.
        """
        if self.game_over:
            return

        self.snake.move()

        if self._is_collision():
            self.game_over = True
            return

        if self.snake.head == self.food.position:
            self.score += 1
            self.snake.grow()
            self.food.spawn(self.snake.body)

    def is_game_over(self) -> bool:
        """
        Checks if the game is over.

        Returns:
            bool: True if the game is over, False otherwise.
        """
        return self.game_over

    def _is_collision(self) -> bool:
        """
        Helper method to check for game-ending collisions.

        A collision occurs if the snake hits the game boundaries or its own body.

        Returns:
            bool: True if a collision occurred, False otherwise.
        """
        # Wall collision
        if (self.snake.head.x >= self.width or self.snake.head.x < 0 or
                self.snake.head.y >= self.height or self.snake.head.y < 0):
            return True

        # Self collision
        if self.snake.check_collision():
            return True

        return False