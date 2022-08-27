import pathlib
import random
from typing import List, Tuple

from PIL import Image

import read_file


def create_paper(size: Tuple[int, int] = (2480, 3508)):
    return Image.new("RGBA", size, color="white")


def get_letter_image(letter: str) -> Image:
    pic_amount: int = 4  # Amount of pictures of each letter
    # There's `pic_amount * 2` pictures of each letter in each folder
    # THe first `pic_amount` images are for uppercase and the last `pic_amount` images are for lowercase letters
    if letter.isupper():
        pic: int = random.randint(1, pic_amount)
    else:
        pic: int = random.randint(pic_amount + 1, pic_amount * 2)
    image: Image = Image.open(f"{pathlib.Path(__file__).parent}\\Characters\\letters\\{letter.upper()}\\{pic}.png")
    image.show()


def main():
    paper = create_paper()
    paper.show()

    contents: List[str] = read_file.get_file_contents()
    for paragraph in contents:
        for letter in paragraph:
            get_letter_image(letter=letter)


if __name__ == '__main__':
    main()
