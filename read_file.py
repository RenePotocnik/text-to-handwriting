import tkinter
from tkinter import filedialog
from typing import List


def get_file():
    """
    Open file explorer, wait for user to open a `.txt` file

    :return: The `.txt` file directory
    """
    print("Open a `.txt` file.", end="\r")
    root = tkinter.Tk()
    root.withdraw()
    file_path: str = filedialog.askopenfilename(filetypes=[("Text File", "*.txt")])
    root.destroy()
    # Clear the last line
    print(" " * 20, end="\r")
    return file_path


def read_file(file_path: str) -> List[str]:
    """
    Read the file on the entered `file_path`, return all lines

    :param file_path: Location of `.txt` file
    :return: List of read lines
    """
    with open(file_path, "r") as file:
        contents: List[str] = file.readlines()
    return contents


def get_lines():
    file_path: str = get_file()
    contents: List[str] = read_file(file_path)
    return contents


if __name__ == '__main__':
    text = get_lines()
    if "y" in input("Print lines? [y/n]\n"
                    "> "):
        print(text)
