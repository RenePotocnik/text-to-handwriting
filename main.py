import pathlib
import random
from typing import List, Tuple, Dict

from PIL import Image

import read_file


misc_chars: Dict[str, str] = {
                ".": "dot",
                "?": "question",
                '"': "quote",
                "/": "slash"
            }


def create_paper(size: Tuple[int, int] = (2480, 3508)):
    return Image.new("RGBA", size, color="white")


def get_char_image(char: str) -> Image:
    pic_amount: int = 4  # Amount of pictures of each char
    # There's `pic_amount * 2` pictures of each char in each folder
    # The first `pic_amount` images are for uppercase and the last `pic_amount` images are for lowercase letters
    try:
        for _ in range(1):

            # Check if character is a number
            if char.isdigit():
                pic: int = random.randint(1, pic_amount)
                path: str = f"{pathlib.Path(__file__).parent}\\Characters\\numbers\\{char}\\{pic}.png"
                break

            # Check if character is a letter
            if char.isalpha():
                pic: int = random.randint(1, pic_amount) if char.isupper() else \
                    random.randint(pic_amount + 1, pic_amount * 2)
                path: str = f"{pathlib.Path(__file__).parent}\\Characters\\letters\\{char.upper()}\\{pic}.png"
                break

            # Check if character is one of the `misc` chars
            if char in "!,-":
                pic: int = random.randint(1, pic_amount)
                path: str = f"{pathlib.Path(__file__).parent}\\Characters\\misc\\{char}\\{pic}.png"
                break
            if char in '.?"/':
                pic: int = random.randint(1, pic_amount)
                path: str = f"{pathlib.Path(__file__).parent}\\Characters\\misc\\{char}\\{pic}.png"
                break
        else:
            print(f"Unknown character: '{char}'")
            return
        return Image.open(path)

    except FileNotFoundError:
        print(f"'{char}' file not found.")


def main():
    paper = create_paper()
    paper.show()
    contents: List[str] = read_file.get_file_contents()
    for paragraph in contents:
        for char in paragraph:
            get_char_image(char=char)


if __name__ == '__main__':
    main()