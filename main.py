import pathlib
import random

from PIL import Image


def create_paper():
    # Create a blank, white sheet of paper
    return Image.new("RGBA", (2480, 3508), color="white")


def get_letter_image(letter: str) -> Image:
    pic_amount: int = 4  # How many pictures of each letter there is
    pic: int = random.randint(1, pic_amount)
    image: Image = Image.open(f"{pathlib.Path(__file__).parent}\\Characters\\letters\\{letter.upper()}\\{pic}.png")
    image.show()


def main():
    paper = create_paper()
    # paper.show()


if __name__ == '__main__':
    main()
