import sys
from abc import abstractmethod
from shutil import get_terminal_size


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
