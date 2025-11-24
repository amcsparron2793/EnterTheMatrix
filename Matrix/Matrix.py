import random
import time
from abc import abstractmethod
from os import system, name as os_name
from shutil import get_terminal_size
import sys


# noinspection PyAbstractClass
class _TerminalFrame:
    """
    Represents a foundational class for building and managing terminal-based visual
    frames with dynamic content.

    Provides essential functionality for creating, maintaining, and rendering a
    buffered display in terminal applications. The class handles terminal size
    detection, cursor manipulation, and character/color rendering for each frame.
    It serves as a base class, allowing specific implementations to inherit and
    extend its functionality.

    Attributes:
        RESET: Class-level constant representing the ANSI escape sequence for resetting
            terminal styles.
        HIDE_CURSOR: Class-level constant containing the ANSI escape sequence to hide
            the cursor in the terminal.
        SHOW_CURSOR: Class-level constant containing the ANSI escape sequence to
            restore the cursor's visibility.
        CURSOR_TOP_LEFT: Class-level constant representing the ANSI escape sequence
            to move the terminal cursor to the top-left corner.
        DEFAULT_TERMINAL_COLUMNS: Class-level constant defining the fallback value
            for the number of terminal columns if detection fails.
        DEFAULT_TERMINAL_LINES: Class-level constant defining the fallback value for
            the number of terminal lines if detection fails.

    Attributes of instances are determined dynamically based on terminal size and
    buffer settings.
    """
    RESET = '\033[0m'
    HIDE_CURSOR = '\033[?25l'
    SHOW_CURSOR = '\033[?25h'
    CURSOR_TOP_LEFT = '\033[H'
    DEFAULT_TERMINAL_COLUMNS = 80
    DEFAULT_TERMINAL_LINES = 24

    def __init__(self, **kwargs):
        self.terminal_columns, self.terminal_lines = self._get_terminal_size()
        self.frame = 0
        self.display = []
        self.colors = []

    @abstractmethod
    def _update_and_draw_columns(self):
        pass

    def _initialize_frame(self):
        self._create_display_buffer()
        self._update_and_draw_columns()

    def _create_display_buffer(self):
        # Create the blank display buffer and a list that will hold the color codes for each character
        self.display = [[' ' for _ in range(self.terminal_columns)] for _ in range(self.terminal_lines)]
        self.colors = [[self.__class__.RESET for _ in range(self.terminal_columns)] for _ in range(self.terminal_lines)]
        return self.display, self.colors

    def _get_terminal_size(self, **kwargs):
        # Get terminal size
        try:
            self.terminal_columns = get_terminal_size().columns
            self.terminal_lines = get_terminal_size().lines
        except (OSError, Exception):
            self.terminal_columns = kwargs.get('columns', self.__class__.DEFAULT_TERMINAL_COLUMNS)
            self.terminal_lines = kwargs.get('lines', self.__class__.DEFAULT_TERMINAL_LINES)
        return self.terminal_columns, self.terminal_lines

    def _check_for_end_of_frame(self, row_idx):
        # end frame with a newline
        if row_idx < self.terminal_lines - 1:
            sys.stdout.write('\n')

    def _build_line(self, row_idx):
        line = ''
        # add each column character to the line
        for col_idx in range(self.terminal_columns):
            line += self.colors[row_idx][col_idx] + self.display[row_idx][col_idx]
        line += self.__class__.RESET
        return line

    def _write_row(self, row_idx):
        line = self._build_line(row_idx)
        sys.stdout.write(line)
        self._check_for_end_of_frame(row_idx)

    def draw_frame(self):
        sys.stdout.write(self.__class__.CURSOR_TOP_LEFT)  # Move cursor to top-left
        # print each row individually
        for row_idx in range(self.terminal_lines):
            self._write_row(row_idx)
        sys.stdout.flush()


class FrameDrawer(_TerminalFrame):
    """
    Manages and draws the matrix-like falling characters animation.

    A FrameDrawer handles the logic for generating and rendering the animation
    of falling characters, inspired by the Matrix movie. Columns in the terminal
    drop characters at different speeds and with varying trail lengths. The class
    utilizes ANSI color codes to create a gradient effect, appearing bright at the
    head of the trail and dimmer at the tail.

    Attributes:
        CHARS (list of str): A collection of characters used for rendering the falling
            trails in the matrix effect.
        GREEN (str): ANSI escape code for standard green color.
        BRIGHT_GREEN (str): ANSI escape code for bright green color.
        DIM_GREEN (str): ANSI escape code for dim green color.

    Methods:
        __init__: Initializes the FrameDrawer instance and its internal column data.
        initialize_columns: Prepares the starting state for the columns, including
            initial positions, speeds, and trail lengths.
        _draw_column_trail: Draws a single column's trail with gradients from bright to dim.
        _check_for_drop_off: Resets a column's state if it has moved off-screen.
        _update_and_draw_columns: Updates the positions of all columns and renders the
            corresponding trails based on their current state.
    """
    CHARS = [
        'ﾊ', 'ﾐ', 'ﾋ', 'ｰ', 'ｳ', 'ｼ', 'ﾅ', 'ﾓ', 'ﾆ', 'ｻ', 'ﾜ', 'ﾂ', 'ｵ', 'ﾘ', 'ｱ', 'ﾎ',
        'ﾃ', 'ﾏ', 'ｹ', 'ﾒ', 'ｴ', 'ｶ', 'ｷ', 'ﾑ', 'ﾕ', 'ﾗ', 'ｾ', 'ﾈ', 'ｽ', 'ﾀ', 'ﾇ', 'ﾍ',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'Z', ':', '.', '"', '=', '*', '+', '-', '<', '>', '¦', '|', 'ﾘ'
    ]

    # ANSI color codes
    GREEN = '\033[92m'
    BRIGHT_GREEN = '\033[38;5;46m'
    DIM_GREEN = '\033[38;5;22m'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drops, self.speeds, self.lengths = self.initialize_columns()

    def _draw_column_trail(self, i):
        # Draw the trail
        for j in range(self.lengths[i]):
            y = self.drops[i] - j
            if 0 <= y < self.terminal_lines:
                self.display[y][i] = random.choice(self.__class__.CHARS)

                # Color gradient: bright at head, dim at tail
                if j == 0:
                    self.colors[y][i] = self.__class__.BRIGHT_GREEN
                elif j < 3:
                    self.colors[y][i] = self.__class__.GREEN
                else:
                    self.colors[y][i] = self.__class__.DIM_GREEN

    def _check_for_drop_off(self, i):
        # self.__class__.RESET column if it's gone off screen
        if self.drops[i] > self.terminal_lines + self.lengths[i]:
            self.drops[i] = 0
            self.speeds[i] = random.uniform(0.5, 1.5)
            self.lengths[i] = random.randint(5, 25)

    def _update_and_draw_columns(self):
        # Update and draw each column
        for i in range(self.terminal_columns):
            column_speed = self.speeds[i]
            # creates blank space between columns
            column_skip_interval = max(1, int(2 / column_speed))

            # if the frame is divisible by the column skip interval,
            # draw a trail, otherwise skip it (shows as a blank column)
            if self.frame % column_skip_interval == 0:
                self.drops[i] += 1

            self._check_for_drop_off(i)
            self._draw_column_trail(i)

    def initialize_columns(self):
        # Initialize columns

        # list of 0's for each column
        drops = [0] * self.terminal_columns

        # speed that each column falls at
        speeds = [random.uniform(0.5, 1.5) for _ in range(self.terminal_columns)]

        # length of each trail
        lengths = [random.randint(5, 25) for _ in range(self.terminal_columns)]

        return drops, speeds, lengths


class InitializeMatrix(FrameDrawer):
    """
    Represents an initial setup and behavior for creating a "Matrix rain"
    effect simulation, inheriting from FrameDrawer.

    This class handles the initialization and management of the Matrix
    rain effect, displaying introductory text, managing clean exit
    procedures, and handling frame advancement and timing.

    Attributes:
        INTRO_TEXT: str
            Static introduction text displayed when starting the Matrix rain
            effect.
    """
    INTRO_TEXT = "Starting Matrix rain effect...\nPress Ctrl+C to exit"

    @classmethod
    def clean_exit(cls):
        print(cls.SHOW_CURSOR)  # Show cursor
        print(cls.RESET)
        print("\n\nExiting Matrix...")
        time.sleep(2)
        system('cls' if os_name == 'nt' else 'clear')

    def _print_intro(self):
        print(self.__class__.INTRO_TEXT)
        time.sleep(2)

    def _sleep_and_advance_frame(self):
        time.sleep(0.05)
        self.frame += 1


class Matrix(InitializeMatrix):
    """
    Provides functionality for managing and displaying a dynamic matrix.

    This class inherits from InitializeMatrix and is used to create and manage
    a dynamic display matrix. The main functionality revolves around creating
    a matrix display and iterating through its frames while handling keyboard
    interrupts for a clean shutdown.
    """
    @classmethod
    def quick_dial_in(cls, **kwargs):
        klass = cls(**kwargs)
        return klass.enter_the_matrix()

    def enter_the_matrix(self):
        try:
            while True:
                self._initialize_frame()
                # self._create_display_buffer()
                # self._update_and_draw_columns()
                self.draw_frame()
                self._sleep_and_advance_frame()

        except KeyboardInterrupt:
            self.clean_exit()


if __name__ == "__main__":
    m = Matrix()
    m.enter_the_matrix()
