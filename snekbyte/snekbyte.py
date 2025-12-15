import argparse
import logging
import sys

import pygame

from .utils import constants as const
from .utils.logger import setup_logging


class App:
    """
    The main application class for the SnekByte game.
    Manages game states, rendering, and user input.
    """

    def __init__(self, args: argparse.Namespace):
        """
        Initializes the App.

        Args:
            args: Command-line arguments parsed by argparse.
        """
        setup_logging()
        pygame.init()
        pygame.display.set_caption("SnekByte")

        self.screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "MAIN_MENU"

        # Settings
        self.speed_level = const.INITIAL_SPEED_LEVEL
        self.wonq_mode = args.wonq

        # Fonts
        self.font_large = pygame.font.SysFont(const.FONT_NAME_MONO, const.FONT_SIZE_LARGE, bold=True)
        self.font_medium = pygame.font.SysFont(const.FONT_NAME_MONO, const.FONT_SIZE_MEDIUM)
        self.font_small = pygame.font.SysFont(const.FONT_NAME_MONO, const.FONT_SIZE_SMALL)

        # Game instance - will be created when 'Play Game' is selected
        self.game = None
        logging.info("SnekByte application initialized.")

    def _render_text(self, text: str, font: pygame.font.Font, color: tuple, center_pos: tuple):
        """
        Renders text on the screen at a specified center position.

        Args:
            text: The string to render.
            font: The pygame Font object to use.
            color: The color of the text.
            center_pos: A tuple (x, y) for the center of the text rectangle.
        """
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=center_pos)
        self.screen.blit(text_surface, text_rect)

    def _draw_main_menu(self, selected_option: int):
        """
        Renders the main menu screen, including the title and options.

        Args:
            selected_option: The index of the currently highlighted menu item.
        """
        self.screen.fill(const.BLACK)

        # Draw ASCII Art Title
        y_offset = 50
        for i, line in enumerate(const.TITLE_ART.strip().split('\n')):
            title_surf = self.font_small.render(line, True, const.GREEN)
            title_rect = title_surf.get_rect(center=(const.SCREEN_WIDTH / 2, y_offset + i * 20))
            self.screen.blit(title_surf, title_rect)

        # Draw Menu Options
        menu_items = ["Play Game", "Settings", "Quit"]
        for i, item in enumerate(menu_items):
            color = const.YELLOW if i == selected_option else const.WHITE
            self._render_text(
                item,
                self.font_medium,
                color,
                (const.SCREEN_WIDTH / 2, 350 + i * 60)
            )
        pygame.display.flip()

    def show_main_menu(self):
        """Handles the logic and rendering for the main menu state."""
        selected_option = 0
        menu_items_count = 3

        while self.state == "MAIN_MENU":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.state = "QUIT"
                if event.type == pygame.KEYDOWN:
                    if event.key in const.KEY_BINDINGS['DOWN']:
                        selected_option = (selected_option + 1) % menu_items_count
                    elif event.key in const.KEY_BINDINGS['UP']:
                        selected_option = (selected_option - 1 + menu_items_count) % menu_items_count
                    elif event.key in const.KEY_BINDINGS['CONFIRM']:
                        if selected_option == 0:  # Play Game
                            self.state = "GAME_START"
                        elif selected_option == 1:  # Settings
                            self.state = "SETTINGS"
                        elif selected_option == 2:  # Quit
                            self.running = False
                            self.state = "QUIT"
                    elif event.key in const.KEY_BINDINGS['QUIT']:
                        self.running = False
                        self.state = "QUIT"

            self._draw_main_menu(selected_option)
            self.clock.tick(15)

    def _draw_settings_menu(self, selected_option: int):
        """
        Renders the settings menu screen.

        Args:
            selected_option: The index of the currently highlighted setting.
        """
        self.screen.fill(const.BLACK)
        self._render_text("Settings", self.font_large, const.WHITE, (const.SCREEN_WIDTH / 2, 100))

        # Speed setting
        speed_text = f"Speed: < {const.SPEED_NAMES[self.speed_level]} >"
        speed_color = const.YELLOW if selected_option == 0 else const.WHITE
        self._render_text(speed_text, self.font_medium, speed_color, (const.SCREEN_WIDTH / 2, 250))

        # Won-Q Mode setting
        wonq_status = "ON" if self.wonq_mode else "OFF"
        wonq_text = f"Won-Q Mode: [ {wonq_status} ]"
        wonq_color = const.YELLOW if selected_option == 1 else const.WHITE
        self._render_text(wonq_text, self.font_medium, wonq_color, (const.SCREEN_WIDTH / 2, 320))

        # Back option
        back_color = const.YELLOW if selected_option == 2 else const.WHITE
        self._render_text("Back", self.font_medium, back_color, (const.SCREEN_WIDTH / 2, 420))

        pygame.display.flip()

    def show_settings_menu(self):
        """Handles the logic and rendering for the settings menu state."""
        selected_option = 0
        menu_items_count = 3
        max_speed_level = len(const.SPEED_LEVELS) - 1

        while self.state == "SETTINGS":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.state = "QUIT"
                if event.type == pygame.KEYDOWN:
                    if event.key in const.KEY_BINDINGS['QUIT']:
                        self.state = "MAIN_MENU"
                    elif event.key in const.KEY_BINDINGS['DOWN']:
                        selected_option = (selected_option + 1) % menu_items_count
                    elif event.key in const.KEY_BINDINGS['UP']:
                        selected_option = (selected_option - 1 + menu_items_count) % menu_items_count
                    elif event.key in const.KEY_BINDINGS['LEFT']:
                        if selected_option == 0:  # Speed
                            self.speed_level = max(0, self.speed_level - 1)
                    elif event.key in const.KEY_BINDINGS['RIGHT']:
                        if selected_option == 0:  # Speed
                            self.speed_level = min(max_speed_level, self.speed_level + 1)
                    elif event.key in const.KEY_BINDINGS['CONFIRM']:
                        if selected_option == 1:  # Won-Q Mode
                            self.wonq_mode = not self.wonq_mode
                        elif selected_option == 2:  # Back
                            self.state = "MAIN_MENU"

            self._draw_settings_menu(selected_option)
            self.clock.tick(15)

    def run(self):
        """The main loop of the application, which delegates to state handlers."""
        while self.running:
            if self.state == "MAIN_MENU":
                self.show_main_menu()
            elif self.state == "SETTINGS":
                self.show_settings_menu()
            elif self.state == "GAME_START":
                # In a future briq, this will instantiate and run the game.
                # For now, it's a placeholder to show the flow is working.
                logging.info(f"Starting game with Speed: {self.speed_level}, Won-Q: {self.wonq_mode}")
                self.state = "MAIN_MENU"  # Go back to main menu for now.
                # To quit after "Play" for testing, uncomment the following:
                # self.running = False
            elif self.state == "QUIT":
                self.running = False

        logging.info("SnekByte application shutting down.")
        pygame.quit()
        sys.exit()