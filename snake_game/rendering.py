import pygame
from typing import Dict, Any, List
from .config import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    BLACK, WHITE, GREEN, RED,
    FONT_SIZE
)

def initialize_screen() -> pygame.Surface:
    """
    Initializes the pygame screen and returns the screen surface.

    Returns:
        pygame.Surface: The main screen surface for drawing.
    """
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake Game')
    return screen

def draw_game(screen: pygame.Surface, game_state: Dict[str, Any]) -> None:
    """
    Renders the entire game state to the screen.

    Args:
        screen (pygame.Surface): The screen to draw on.
        game_state (Dict[str, Any]): The current state of the game.
    """
    screen.fill(BLACK)
    draw_snake(screen, game_state.get('snake_body', []))
    if 'food_pos' in game_state:
        draw_food(screen, game_state['food_pos'])
    draw_hud(screen, game_state)

def draw_snake(screen: pygame.Surface, snake_body: List[pygame.Rect]) -> None:
    """
    Draws the snake on the screen.

    Args:
        screen (pygame.Surface): The screen to draw on.
        snake_body (List[pygame.Rect]): A list of Rects representing the snake's body.
    """
    for segment in snake_body:
        pygame.draw.rect(screen, GREEN, segment)

def draw_food(screen: pygame.Surface, food_pos: pygame.Rect) -> None:
    """
    Draws the food on the screen.

    Args:
        screen (pygame.Surface): The screen to draw on.
        food_pos (pygame.Rect): A Rect representing the food's position.
    """
    pygame.draw.rect(screen, RED, food_pos)

def draw_hud(screen: pygame.Surface, game_state: Dict[str, Any]) -> None:
    """
    Draws the heads-up display (score and speed).

    Args:
        screen (pygame.Surface): The screen to draw on.
        game_state (Dict[str, Any]): The current state of the game, including score and speed level.
    """
    score = game_state.get('score', 0)
    speed_level = game_state.get('speed_level', 0)
    
    font = pygame.font.Font(None, FONT_SIZE)
    
    # Score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (5, 5))

    # Speed
    speed_text = font.render("Speed:", True, WHITE)
    screen.blit(speed_text, (5, 40))
    
    # Speed bar
    for i in range(10):
        color = GREEN if i <= speed_level else WHITE
        pygame.draw.rect(screen, color, (100 + i * 20, 45, 15, 15))

    # Speed hint
    hint_text = font.render("< >", True, WHITE)
    screen.blit(hint_text, (100 + 10 * 20 + 10, 40))

def display_game_over(screen: pygame.Surface, score: int, selected_option: str) -> None:
    """
    Displays the game over message and menu.

    Args:
        screen (pygame.Surface): The screen to draw on.
        score (int): The final score.
        selected_option (str): The currently selected menu option ('Retry' or 'Quit').
    """
    screen.fill(BLACK)
    
    # Game Over text
    font = pygame.font.Font(None, FONT_SIZE * 2)
    game_over_text = font.render("Game Over", True, WHITE)
    text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
    screen.blit(game_over_text, text_rect)

    # Final score
    score_font = pygame.font.Font(None, FONT_SIZE)
    final_score_text = score_font.render(f"Final Score: {score}", True, WHITE)
    score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(final_score_text, score_rect)

    # Menu options
    retry_color = GREEN if selected_option == "Retry" else WHITE
    quit_color = GREEN if selected_option == "Quit" else WHITE

    retry_text = score_font.render("Retry", True, retry_color)
    retry_rect = retry_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + FONT_SIZE * 2))
    screen.blit(retry_text, retry_rect)

    quit_text = score_font.render("Quit", True, quit_color)
    quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + FONT_SIZE * 3))
    screen.blit(quit_text, quit_rect)