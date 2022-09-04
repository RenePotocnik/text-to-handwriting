import os
from pathlib import Path


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


create_directories()
