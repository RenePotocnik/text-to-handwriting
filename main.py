from PIL import Image


def create_paper():
    # Create a blank, white sheet of paper
    return Image.new("RGBA", (2480, 3508), color="white")


def main():
    paper = create_paper()
    paper.show()


if __name__ == '__main__':
    main()
