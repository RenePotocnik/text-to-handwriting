import datetime
import pathlib
import random
import time
import tkinter
from tkinter import filedialog
from typing import List, Tuple, Dict, Optional

from PIL import Image

# Characters that cannot be inside a file path
misc_chars: Dict[str, str] = {
    ".": "dot",
    "?": "question",
    '"': "quote",
    "/": "slash"
}


def create_paper(size: Tuple[int, int], background_image=None) -> Image:
    """
    Create a white PIL Image object, of specified size.

    :param size: The size of the paper
    :param background_image: OPTIONAL; The background image of the paper. THe image will be resized to paper `size`
    :return: The paper - PIL.Image
    """
    paper: Image = Image.new("RGBA", size, color="white")
    # If there's a background image, resize it to the same size as the paper
    if background_image:
        paper.paste(background_image.scale(size))
    return paper


def get_file(suffix: str = ".txt") -> str:
    """
    Open file explorer, wait for user to open a `suffix` file

    :return: The selected file directory
    """
    print(f"Open a `{suffix}` file.", end="\r")
    root = tkinter.Tk()
    root.attributes("-topmost", 1)
    root.withdraw()
    file_path: str = filedialog.askopenfilename(filetypes=[("Select File", f"*{suffix}")])
    root.destroy()
    # Clear the last line
    print(" " * 20, end="\r")
    return file_path


def progress_update(current: int, full: int, prefix='Progress', suffix='', length=50) -> None:
    """
    Display a progress bar in the console

    :param current: The current value
    :param full: The full value
    :param prefix: Text in-front of the progress bar
    :param suffix: Text behind the progress bar
    :param length: The length of the progress bar
    """
    completed = int(length * current // full)
    print(f'\r{prefix}'
          f' |{"#" * completed + " " * (length - completed)}| '
          f'{f"{100 * (current / float(full)):.2f}"}% '
          f'{suffix}', end="\r")

    # Print New Line on Complete
    if current == full:
        print(" " * (length + 30), end="\r")


def read_file(file_path: str) -> List[str]:
    """
    Read the file on the entered `file_path`, return a list of all the paragraphs

    :param file_path: Location of `.txt` file
    :return: List of read lines
    """
    with open(file_path, "r", encoding="UTF-8") as file:
        contents: List[str] = file.readlines()
    return contents


def get_char_image(char: str) -> Optional['Image']:
    """
    Locate the image of the passed `char`. Return a png PIL.Image of the char

    :param char: The character whose image were searching for
    :return:
    """
    pic_amount: int = 4  # Amount of pictures of each char
    # There's `pic_amount * 2` pictures of each char in each folder
    # The first half are for uppercase letters, the second half are for lowercase letters
    pic: int = random.randint(1, pic_amount)  # Pick a random image
    try:
        # Check if character is a number
        if char.isdigit():
            path: str = f"{pathlib.Path(__file__).parent}\\Characters\\numbers\\{char}\\{pic}.png"

        # Check if character is a letter
        elif char.isalpha():
            path: str = f"{pathlib.Path(__file__).parent}\\Characters\\letters\\{char.upper()}\\" \
                        f"{pic if char.isupper() else random.randint(pic_amount + 1, pic_amount * 2)}.png"

        # Check if character is one of the chars that can be included in a file path
        elif char in "!,-":
            path: str = f"{pathlib.Path(__file__).parent}\\Characters\\misc\\{char}\\{pic}.png"

        # Check if character is one of the chars in `misc_chars` - cannot be in file path
        elif char in misc_chars:
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
            # The char could not be sorted into one of the groups - unknown character
            print(f"Unknown character: '{char}'.")
            return None
        # Open and return the image of the char
        return Image.open(path)

    # The file of the char was not found though it did fit in one of the categories
    except FileNotFoundError:
        print(f"'{char}' not found")


def place_on_paper(char: Image, coords: Tuple[int, int], paper: Image, letter: str = None):
    """
    Place a smaller image (`char`) on a larger image (`paper`) at the given coordinates (`coords`)

    :param char: The smaller image of a char
    :param coords: The coordinates, where to place the char image
    :param paper: The paper/main image where to place the char
    :param letter: The current letter, used to determine letter position (e.g.: g, j have to be placed further down)
    """
    char_height: int = 50  # The average height of the char - to align them to the bottom of a line
    kerning_variation: int = 5  # How much should the letters vary in horizontal placement - makes it more realistic
    height_variation: int = 5  # How much should the letters vary in vertical placement - makes it more realistic
    x: int = coords[0] + random.randint(int(f"-{kerning_variation}"), kerning_variation)
    y: int = coords[1] + abs(char_height - char.height) + random.randint(int(f"-{height_variation}"), height_variation)

    # If the letter has a "tail", place it lower on the line
    if letter in "pgjy,":
        y: int = coords[1] + abs(char_height - int(char.height / 2))\
                 + random.randint(int(f"-{height_variation}"), height_variation)

    paper.paste(im=char, box=(x, y), mask=char)
    # Image.Image.paste(paper, char, coords, char)


def save_pages(pages: List[any], file_path: str) -> None:
    """
    Prompt user to select folder to save pages.
    If multiple pages, save in following format: `{file_name}_{page_number}.png`
    General save format: `{path}/HW_{file_name}_{page}-{time}`

    :param pages: A list of all the pages
    :param file_path: The file path where to save the pages
    """
    # Get save location
    root = tkinter.Tk()
    root.attributes("-topmost", 1)
    root.withdraw()
    paper_path_template = filedialog.askdirectory()
    root.destroy()

    # If no location was selected, don't save
    if not paper_path_template:
        print("Closing without saving.")
        return
    paper_path_template += f"/HW_{pathlib.Path(file_path).stem}_pages-{{page:}}{{time:%H-%M-%S}}.png"
    for n, page in enumerate(pages):
        page.save(paper_path_template.format(page=n, time=datetime.datetime.now()))
    print("Pages saved to ", paper_path_template.format(page=f"0-{len(pages)}_", time=datetime.datetime.now()))


def main():
    avg_char_width: int = 30  # The average width of a char
    new_line: int = 70  # Spacing between lines
    word_spacing: int = 40  # Spacing between individual words or letters
    x_margin: int = 100  # Side margin
    y_margin: int = 100  # Top margin

    paper_size: Tuple[int, int] = (2480, 3508)  # Size of the main paper in pixels (A4)

    background_image = None
    if "y" in input("Add a Background to a paper? [y/n]\n> ").lower():
        print("Select a paper background image. Must be '2480x3508'.")
        background_image = Image.open(get_file(suffix=".png"))
    pages: List[Image] = [create_paper(size=(2480, 3508),
                                       background_image=background_image)]
    cur_page: int = 0
    file_path = get_file()
    contents: List[str] = read_file(file_path)

    def if_new_page() -> bool:
        if y >= paper_size[1] - y_margin:
            pages.append(create_paper(size=(2480, 3508),
                                      background_image=background_image))
            return True
        return False

    x: int = x_margin
    y: int = y_margin
    for n, line in enumerate(contents):
        for word in line.strip().split(" "):
            if len(word) * avg_char_width + x >= paper_size[0] - x_margin:
                y += new_line
                x = x_margin
                if if_new_page():
                    cur_page += 1
                    y = y_margin
                    x = x_margin
            for char in word:
                char_img: Image = get_char_image(char=char)
                place_on_paper(char=char_img, coords=(x, y), paper=pages[cur_page], letter=char)
                x += char_img.width
            x += word_spacing
        y += new_line
        x = x_margin
        if if_new_page():
            cur_page += 1
            y = y_margin
            x = x_margin
        progress_update(current=n, full=len(contents))
    print(" " * 80, end="\r")

    save_pages(pages=pages, file_path=file_path)


if __name__ == '__main__':
    main()
