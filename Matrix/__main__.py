from os import chdir

try:
    from . import EnterTheMatrix, ROOT_DIR
except (ImportError, ModuleNotFoundError):
    from Matrix import EnterTheMatrix, ROOT_DIR

def main():
    chdir(ROOT_DIR)
    matrix = EnterTheMatrix()
    matrix.jack_in()

if __name__ == "__main__":
    #print(ROOT_DIR)
    main()