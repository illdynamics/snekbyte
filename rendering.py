import pygame
from typing import Dict, Any, List
from settings import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
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
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
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
    draw_score(screen, game_state.get('score', 0))
    pygame.display.flip()

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

def draw_score(screen: pygame.Surface, score: int) -> None:
    """
    Draws the score on the screen.

    Args:
        screen (pygame.Surface): The screen to draw on.
        score (int): The current score.
    """
    font = pygame.font.Font(None, FONT_SIZE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (5, 5))

def display_game_over(screen: pygame.Surface, score: int) -> None:
    """
    Displays the game over message.

    Args:
        screen (pygame.Surface): The screen to draw on.
        score (int): The final score.
    """
    screen.fill(BLACK)
    font = pygame.font.Font(None, FONT_SIZE * 2)
    game_over_text = font.render("Game Over", True, WHITE)
    text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - FONT_SIZE))
    screen.blit(game_over_text, text_rect)

    score_font = pygame.font.Font(None, FONT_SIZE)
    final_score_text = score_font.render(f"Final Score: {score}", True, WHITE)
    score_rect = final_score_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + FONT_SIZE))
    screen.blit(final_score_text, score_rect)

    pygame.display.flip()