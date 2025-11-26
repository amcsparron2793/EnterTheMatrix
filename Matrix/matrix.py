import time
from os import system, name as os_name

from Matrix.draw_frame import FrameDrawer, TextFormatter


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
    EXIT_TEXT = "Exiting Matrix..."

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text_formatter = TextFormatter(self.terminal_columns)

    def _print_error_screen(self):
        system('cls' if os_name == 'nt' else 'clear')
        self._initialize_frame(error=True)
        self.draw_frame()
        full_err_text = self.text_formatter.format_as_text_box(self.__class__.EXIT_TEXT, color=self.__class__.RED,
                                                               dash_char=self.__class__.CHARS)
        print(f"\n{full_err_text}")

    def clean_exit(self):
        print(self.__class__.SHOW_CURSOR)  # Show cursor
        print(self.__class__.RESET)

        self._print_error_screen()

        time.sleep(2)
        system('cls' if os_name == 'nt' else 'clear')

    def _print_intro(self):
        formatted_intro = self.text_formatter.format_as_text_box(self.__class__.INTRO_TEXT, color=self.__class__.GREEN,
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
