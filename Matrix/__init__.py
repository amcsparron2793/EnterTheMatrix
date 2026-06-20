from pathlib import Path

# FIXME: implement me?
ROOT_DIR = Path(__file__).parent

try:
    from .terminal import _TerminalFrame
    from .draw_frame import FrameDrawer
    from .matrix import InitializeMatrix, EnterTheMatrix
except (ImportError, ModuleNotFoundError):
    from Matrix.terminal import _TerminalFrame
    from Matrix.draw_frame import FrameDrawer
    from Matrix.matrix import InitializeMatrix, EnterTheMatrix
