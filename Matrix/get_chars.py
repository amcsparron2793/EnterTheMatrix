from json import dump, load
from pathlib import Path
from typing import Union

try:
    from . import ROOT_DIR
except (ImportError, ModuleNotFoundError):
    from Matrix import ROOT_DIR

BACKUP_CHARS = [
        'ﾊ', 'ﾐ', 'ﾋ', 'ｰ', 'ｳ', 'ｼ', 'ﾅ', 'ﾓ', 'ﾆ', 'ｻ', 'ﾜ', 'ﾂ', 'ｵ', 'ﾘ', 'ｱ', 'ﾎ',
        'ﾃ', 'ﾏ', 'ｹ', 'ﾒ', 'ｴ', 'ｶ', 'ｷ', 'ﾑ', 'ﾕ', 'ﾗ', 'ｾ', 'ﾈ', 'ｽ', 'ﾀ', 'ﾇ', 'ﾍ',
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'Z', ':', '.', '"', '=', '*', '+', '-', '<', '>', '¦', '|', 'ﾘ'
    ]


class GetChars:
    DEFAULT_CHARS_PATH = Path(ROOT_DIR /'Misc_Program_Files' / 'chars.json')
    DEFAULT_CHARS_KEY = 'CHARS'
    DEFAULT_CHAR_ENCODING = 'utf-8'


    @classmethod
    def write_chars(cls, **kwargs):
        chars_path = Path(kwargs.get('chars_path', cls.DEFAULT_CHARS_PATH))
        chars_path.parent.mkdir(parents=True, exist_ok=True)

        chars_key = kwargs.get('chars_key', cls.DEFAULT_CHARS_KEY)

        with open(chars_path, "w") as f:
            chars_dict = {chars_key: BACKUP_CHARS}
            dump(chars_dict, f, indent=4)
            print(f"Wrote backup chars to {chars_path}")
            return chars_dict[chars_key]

    @classmethod
    def read_chars(cls, **kwargs) -> Union[list, dict]:
        chars_path = kwargs.get('chars_path', cls.DEFAULT_CHARS_PATH)
        encoding = kwargs.get('encoding', cls.DEFAULT_CHAR_ENCODING)
        chars_key = kwargs.get('chars_key', cls.DEFAULT_CHARS_KEY)
        write_file_if_missing = kwargs.get('write_file_if_missing', True)

        try:
            with open(chars_path, "r", encoding=encoding) as f:
                chars = load(f)
                print(f"loaded chars dict from {chars_path}")
                return chars[chars_key]
        except KeyError:
            print(f"Error: Key '{chars_key}' not found in the JSON file.")
            print("returning loaded json in full")
            return chars
            # exit(1)
        except FileNotFoundError:
            if not write_file_if_missing:
                raise FileNotFoundError(f"Error: File '{chars_path}' not found.")
            else:
                return cls.write_chars(chars_path=chars_path)
            return BACKUP_CHARS
            # exit(1)
        except Exception as e:
            raise IOError(f"Error reading file '{chars_path}': {e}")
            # exit(1)
