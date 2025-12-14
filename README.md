# Snake Game

This is a classic snake game built with Python and Pygame.

### Quickstart

1.  **Install Dependencies:**
    This will install `pygame`, the library used for the game.
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Game:**
    This command starts the game.
    ```bash
    python main.py
    ```

3.  **How to Play:**
    *   Use the **Arrow Keys** to change the snake's direction.
    *   Eat the food to grow longer and increase your score.
    *   Avoid running into the walls or the snake's own body.
    *   Press the **ESC key** to quit.

### How it Works

*   **`main.py`**: The entry point that runs the main game loop.
*   **`snake_game/core.py`**: Contains the core game logic, like snake movement and collision.
*   **`snake_game/rendering.py`**: Handles drawing the snake, food, and score.
*   **`snake_game/input_handling.py`**: Manages player controls from the keyboard.
*   **`snake_game/config.py`**: Stores game settings like screen size and speed.
