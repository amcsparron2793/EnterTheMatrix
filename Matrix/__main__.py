try:
    from . import EnterTheMatrix
except (ImportError, ModuleNotFoundError):
    from Matrix import EnterTheMatrix

def main():
    # chdir(ROOT_DIR)
    matrix = EnterTheMatrix()
    matrix.jack_in()

if __name__ == "__main__":
    #print(ROOT_DIR)
    main()