import os
from pathlib import Path

import cv2
import numpy as np

SUPPORTED_CHARS: str = (
    "abcčdefghijklmnopqrsštuvwxyzž"
    "ABCČDEFGHIJKLMNOPQRSŠTUVWXYZŽ"
    "0123456789"
    r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""  # Raw string (r) + """literal string"""
)


def create_directories(main_folder: str = "Characters_Test"):
    main_dir = Path(__file__).parent.joinpath(main_folder)
    print(f"Building character database in '{main_dir}' ... ", end="")
    for c in SUPPORTED_CHARS:
        dir_name = str(ord(c))
        # print(f"Creating directory '{dir_name}' for '{c}' ... ")
        os.makedirs(main_dir.joinpath(dir_name), exist_ok=True)
    print("✓")


def sharpen_image(image):
    kernel_sharpening = np.array([[-1, -1, -1],
                                  [-1, 9, -1],
                                  [-1, -1, -1]])
    return cv2.filter2D(image, -1, kernel_sharpening)


def make_transparent(image, threshold: int = 100):
    image[np.where(np.all(image[..., :3] > threshold, -1))] = 0


def show_image(name, current_image, wait: bool = False):
    cv2.imshow(name, current_image)
    if not wait:
        cv2.waitKey(0)


def main():
    image = cv2.imread(r"G:\My Drive\Programs\text-to-handwriting\Character_Grid.png")
    show_image("Original image", image, wait=True)

    # Make grayscale
    og_image = image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # kernel = np.ones((5, 5), np.uint8)
    # image = cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, kernel)

    # Slightly blur the image
    image = cv2.medianBlur(image, 3)

    # Canny
    region_of_interest = cv2.bitwise_not(image)
    outlined_image = cv2.Canny(region_of_interest, 100, 200)

    # make_transparent(image)
    thresh = cv2.adaptiveThreshold(src=image, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   thresholdType=cv2.THRESH_BINARY, blockSize=61, C=20)

    kernel = np.ones((7, 7), np.uint8)
    gradient = cv2.morphologyEx(thresh, cv2.MORPH_GRADIENT, kernel)
    contours, hierarchy = cv2.findContours(gradient, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(og_image, contours, -1, (0, 255, 0), 2)

    show_image("New Image", og_image)

    cv2.destroyAllWindows()


main()
