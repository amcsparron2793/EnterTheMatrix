import time
import random
from os import system, name as os_name

from Matrix.draw_frame import FrameDrawer


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
    #INTRO_TEXT = """---------------\n| Starting Matrix rain effect... | \n| Press Ctrl+C to exit |\n---------------\n"""
    INTRO_TEXT = "Starting Matrix rain effect...\nPress Ctrl+C to exit"
    EXIT_TEXT = "Exiting Matrix..."

    def _text_box_border(self, line_length: int = None, dash_char='-', **kwargs):
        if kwargs.get('force_basic_dash', False):
            dash_char = '-'
        if line_length is None:
            line_length = self.terminal_columns

        return (' '.join([random.choice(self.__class__.CHARS)
                          for _ in range(line_length)])
                if isinstance(dash_char, list) else dash_char * line_length)

    def format_text_box(self, text, color=None, dash_char='-', **kwargs):
        """Format text with decorative lines and centering"""
        if color is None:
            color = self.__class__.GREEN

        lines = text.split('\n')
        border_length = kwargs.get('border_length', len(max(lines)))

        # Create top border
        border = self._text_box_border(line_length=border_length,
                                       dash_char=dash_char, **kwargs)
        full_formatted_border = f"{color}{self.center_string(border)}{self.__class__.RESET}"

        # Build formatted output
        # noinspection PyListCreation
        output = []
        output.append(full_formatted_border)

        for line in lines:
            centered_line = self.center_string(line)
            output.append(f"{color}{centered_line}{self.__class__.RESET}")

        output.append(full_formatted_border)

        return '\n'.join(output)

    def center_string(self, string: str) -> str:
        return f"{string:^{self.terminal_columns}}"

    def _print_error_screen(self):
        system('cls' if os_name == 'nt' else 'clear')
        self._initialize_frame(error=True)
        self.draw_frame()
        full_err_text = self.format_text_box(self.__class__.EXIT_TEXT,
                                             color=self.__class__.RED,
                                             dash_char=self.__class__.CHARS)
        print(f"\n{full_err_text}")

    def clean_exit(self):
        print(self.__class__.SHOW_CURSOR)  # Show cursor
        print(self.__class__.RESET)

        self._print_error_screen()

        time.sleep(2)
        system('cls' if os_name == 'nt' else 'clear')

    def _print_intro(self):
        formatted_intro = self.format_text_box(self.__class__.INTRO_TEXT,
                                               dash_char=self.__class__.CHARS)
        print(formatted_intro)
        time.sleep(2)

    def _sleep_and_advance_frame(self):
        time.sleep(0.05)
        self.frame += 1


class EnterTheMatrix(InitializeMatrix):
    """
    Provides functionality for managing and displaying a dynamic matrix.

    This class inherits from InitializeMatrix and is used to create and manage
    a dynamic display matrix. The main functionality revolves around creating
    a matrix display and iterating through its frames while handling keyboard
    interrupts for a clean shutdown.
    """

    @classmethod
    def quick_jack_in(cls, **kwargs):
        klass = cls(**kwargs)
        return klass.jack_in()

    def jack_in(self):
        self._print_intro()
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
    m = EnterTheMatrix()
    m.jack_in()
