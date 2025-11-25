import random

from Matrix.terminal import _TerminalFrame


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
