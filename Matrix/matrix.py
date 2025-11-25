import time
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
