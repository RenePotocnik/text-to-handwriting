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


def create_paper(size: Tuple[int, int]):
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


def progress_update(current: int, full: int, prefix='Progress', suffix='', length=50) -> None:
    """
    Display a progress bar in the console
    :param current: The `y` value of the image
    :param full: The image
    :param prefix: Optional: Text in-front of the progress bar
    :param suffix: Optional: Text behind the progress bar
    :param length: Optional: The length of the progress bar
    """
    completed = int(length * current // full)
    empty = length - completed
    bar = "#" * completed + " " * empty
    percent = f"{100 * (current / float(full)):.2f}"
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end="\r")

    # Print New Line on Complete
    if current == full:
        print(" " * (length + 30), end="\r")


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
            if char == ".":
                path: str = f"{pathlib.Path(__file__).parent}\\Characters\\misc\\dot\\{pic}.png"
            elif char == "?":
                path: str = f"{pathlib.Path(__file__).parent}\\Characters\\misc\\question\\{pic}.png"
            elif char == '"':
                path: str = f"{pathlib.Path(__file__).parent}\\Characters\\misc\\quote\\{pic}.png"
            elif char == "/":
                path: str = f"{pathlib.Path(__file__).parent}\\Characters\\misc\\slash\\{pic}.png"
            else:
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
    char_height: int = 50
    kerning_variation: int = 5
    height_variation: int = 5
    x: int = coords[0] + random.randint(int(f"-{kerning_variation}"), kerning_variation)
    y: int = coords[1] + abs(char_height - char.height) + random.randint(int(f"-{height_variation}"), height_variation)

    paper.paste(im=char, box=(x, y), mask=char)
    # Image.Image.paste(paper, char, coords, char)


def main():
    kerning: int = 30  # Spacing between individual letters
    new_line: int = 70  # Spacing between lines
    x_margin: int = 100  # Side margin
    y_margin: int = 100  # Top margin

    paper_size: Tuple[int, int] = (2480, 3508)  # Size of the main paper in pixels (A4)

    paper = create_paper(size=(2480, 3508))
    # paper.show()
    x, y = x_margin, y_margin
    prev_char = None
    file_path = get_file()
    contents: List[str] = read_file(file_path)
    for n, paragraph in enumerate(contents):
        y += new_line
        x = x_margin
        for char in paragraph.strip():
            x += prev_char.width if prev_char else kerning
            if x >= paper_size[0] - x_margin:
                y += new_line
                x = x_margin
                continue
            char: Image = get_char_image(char=char)
            if char == "space":
                x += kerning
                continue
            place_on_paper(char=char, coords=(x, y), paper=paper)
            prev_char: Image = char
        progress_update(current=n, full=len(contents))
    print(" " * 80, end="\r")

    paper.show()

    # Get save location
    root = tkinter.Tk()
    root.attributes("-topmost", 1)
    root.withdraw()
    paper_path = filedialog.askdirectory() + "/HW_" + str(pathlib.Path(file_path).stem) + ".png"
    root.destroy()

    # If no location was selected, don't save
    if paper_path[0] == "/":
        print("Closing without saving.")
        return
    paper.save(paper_path)
    print("Image saved to ", paper_path)


if __name__ == '__main__':
    main()
