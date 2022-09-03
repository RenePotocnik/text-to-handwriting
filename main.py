import pathlib
import random
import tkinter
from tkinter import filedialog
from typing import List, Tuple, Dict, Optional

from PIL import Image


misc_chars: Dict[str, str] = {
                ".": "dot",
                "?": "question",
                '"': "quote",
                "/": "slash"
            }


def create_paper(size: Tuple[int, int] = (2480, 3508)):
    return Image.new("RGBA", size, color="white")


def get_file() -> str:
    """
    Open file explorer, wait for user to open a `.txt` file

    :return: The `.txt` file directory
    """
    print("Open a `.txt` file.", end="\r")
    root = tkinter.Tk()
    root.withdraw()
    root.attributes("-topmost", 1)
    file_path: str = filedialog.askopenfilename(filetypes=[("Text File", "*.txt")])
    root.destroy()
    # Clear the last line
    print(" " * 20, end="\r")
    return file_path


def read_file(file_path: str) -> List[str]:
    """
    Read the file on the entered `file_path`, return a list of all the paragraphs

    :param file_path: Location of `.txt` file
    :return: List of read lines
    """
    with open(file_path, "r") as file:
        contents: List[str] = file.readlines()
    return contents


def get_char_image(char: str) -> Optional['Image']:
    pic_amount: int = 4  # Amount of pictures of each char
    # There's `pic_amount * 2` pictures of each char in each folder
    # The first `pic_amount` images are for uppercase and the last `pic_amount` images are for lowercase letters
    try:
        # Check if character is a number
        if char.isdigit():
            pic: int = random.randint(1, pic_amount)
            path: str = f"{pathlib.Path(__file__).parent}\\Characters\\numbers\\{char}\\{pic}.png"
        # Check if character is a letter
        elif char.isalpha():
            pic: int = random.randint(1, pic_amount) if char.isupper() else \
                random.randint(pic_amount + 1, pic_amount * 2)
            path: str = f"{pathlib.Path(__file__).parent}\\Characters\\letters\\{char.upper()}\\{pic}.png"
        # Check if character is one of the `misc` chars
        elif char in "!,-":
            pic: int = random.randint(1, pic_amount)
            path: str = f"{pathlib.Path(__file__).parent}\\Characters\\misc\\{char}\\{pic}.png"
        elif char in '.?"/':
            pic: int = random.randint(1, pic_amount)
            path: str = f"{pathlib.Path(__file__).parent}\\Characters\\misc\\{char}\\{pic}.png"
        elif char == " ":
            return "space"
        else:
            print(f"Unknown character: '{char}'")
            return None
        return Image.open(path)

    except FileNotFoundError:
        print(f"'{char}' file not found.")


def place_on_paper(char: Image, coords: Tuple[int, int], paper: Image):
    """
    Place a smaller image (`char`) on a larger image (`paper`) at the given coordinates (`coords`)

    :param char: The smaller image of a char
    :param coords: The coordinates, where to place the char image
    :param paper: The paper/main image where to place the char
    """
    paper.paste(im=char, box=coords, mask=char)
    # Image.Image.paste(paper, char, coords, char)


def main():
    kerning: int = 30  # Spacing between individual letters
    new_line: int = 40  # Spacing between lines
    x_margin: int = 50  # Side margin
    y_margin: int = 50  # Top margin

    paper = create_paper()
    # paper.show()
    x, y = x_margin, y_margin
    contents: List[str] = read_file(get_file())
    for paragraph in contents:
        y += new_line
        x = x_margin
        for char in paragraph.strip():
            x += kerning
            char: str = get_char_image(char=char)
            if char == "space":
                x += kerning
                continue
            place_on_paper(char=char, coords=(x, y), paper=paper)

    paper.show()


if __name__ == '__main__':
    main()
