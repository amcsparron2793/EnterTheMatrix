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
    RED = '\033[91m'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drops, self.speeds, self.lengths = self.initialize_columns()

    def _character_within_terminal_bounds(self, vert_pos: int) -> bool:
        return 0 <= vert_pos < self.terminal_lines

    def _set_display_character(self, vert_pos: int, col_index: int):
        # set display character to a random character from CHARS
        # in the appropriate slot of the display list
        self.display[vert_pos][col_index] = random.choice(self.__class__.CHARS)

    def _set_character_color(self, vert_pos: int, col_index: int, trail_length: int, **kwargs):
        # Color gradient: bright at head, dim at tail
        # set the color of the character in the
        # color's list to the same slot as the display list
        if kwargs.get('error'):
            self.colors[vert_pos][col_index] = self.__class__.RED
            return
        if trail_length == 0:
            self.colors[vert_pos][col_index] = self.__class__.BRIGHT_GREEN
        elif trail_length < 3:
            self.colors[vert_pos][col_index] = self.__class__.GREEN
        else:
            self.colors[vert_pos][col_index] = self.__class__.DIM_GREEN

    def _draw_and_color_character(self, col_index: int, trail_length: int, **kwargs):
        vert_pos = self.drops[col_index] - trail_length
        if self._character_within_terminal_bounds(vert_pos):
            self._set_display_character(vert_pos, col_index)
            self._set_character_color(vert_pos, col_index, trail_length, **kwargs)

    def _draw_column_trail(self, col_index: int, **kwargs):
        # Draw the trail
        for trail_length in range(self.lengths[col_index]):
            self._draw_and_color_character(col_index, trail_length, **kwargs)

    def _reset_column(self, col_index):
        self.drops[col_index] = 0
        # get new speed and length for the column
        self.speeds[col_index] = random.uniform(0.5, 1.5)
        self.lengths[col_index] = random.randint(5, 25)

    def _check_for_drop_off(self, col_index):
        # self.__class__.RESET column if it's gone off screen
        drop_position = self.drops[col_index]
        max_length_for_terminal = self.terminal_lines + self.lengths[col_index]
        if drop_position > max_length_for_terminal:
            self._reset_column(col_index)

    def update_and_draw_columns(self, **kwargs):
        # Update and draw each column
        for col_index in range(self.terminal_columns):
            column_speed = self.speeds[col_index]
            # creates blank space between columns
            column_skip_interval = max(1, int(2 / column_speed))

            # if the frame is divisible by the column skip interval,
            # draw a trail, otherwise skip it (shows as a blank column)
            if self.frame % column_skip_interval == 0:
                self.drops[col_index] += 1

            self._check_for_drop_off(col_index)
            self._draw_column_trail(col_index, **kwargs)

    def initialize_columns(self):
        # Initialize columns

        # list of 0's for each column
        drops = [0] * self.terminal_columns
        # speed that each column falls at
        speeds = [random.uniform(0.5, 1.5) for _ in range(self.terminal_columns)]
        # length of each trail
        lengths = [random.randint(5, 25) for _ in range(self.terminal_columns)]

        return drops, speeds, lengths
