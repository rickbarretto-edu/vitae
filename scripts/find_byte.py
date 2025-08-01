r"""Find some byte in a file.

Since I had a lot of issues with Python's charmap,
I've created this script to easily find where some byte
is returning an UTF-8 error.

This scripts helps you to inspect any file and then fix the encoding manually.

When Use
--------

You may want use this script when get an exception like:


        "C:\\Users\\{User}\\AppData\\Local\\Programs\\Python\\{PythonVersion}\\Lib\\pathlib.py", line 1028, in read_text
        return f.read()
            ^^^^^^^^
        File "C:\\Users\\{User}\\AppData\\Local\\Programs\\Python\\{PythonVersion}\\Lib\\encodings\\cp1252.py", line 23, in decode
            return codecs.charmap_decode(input,self.errors,decoding_table)[0]

Usage
-----

Make sure this is installed with:

        poetry install

Then run with:

        poetry run find-byte --byte [byte] --file [file]

Examples
--------
        poetry run find-byte --byte 0x70 --file vitae/features/researchers/templates/search/FiltersAside.jinja

"""  # noqa: E501

import argparse
from pathlib import Path
from typing import NamedTuple

NEWLINE = b"\n"

class Ocurrence(NamedTuple):
    line: int
    column: int
    position: int


def occurrences(path: Path, target_byte: int) -> list[Ocurrence]:
    occurrences = []
    with path.open("rb") as file:
        line = 1
        column = 1
        position = 0

        while current_byte := file.read(1):
            if current_byte == bytes([target_byte]):
                occurrences.append((line, column, position))

            if current_byte == NEWLINE:
                line += 1
                column = 1
            else:
                column += 1

            position += 1

    return occurrences


def byte_as_int(value) -> int:
    if value.startswith("0x"):
        return int(value, 16)
    return int(value)


def vscode_openable(path: Path, line: int, col: int) -> str:
    return f"{path}:{line}:{col}-{col + 1}"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Find a byte in a file with line/column output.",
    )
    parser.add_argument("-f", "--file", required=True, help="Path to the file")
    parser.add_argument(
        "-b",
        "--byte",
        required=True,
        type=byte_as_int,
        help="Target byte (e.g., 0x81 or 129)",
    )

    cli_arguments = parser.parse_args()

    target_file = Path(cli_arguments.file)
    target_byte: int = cli_arguments.byte

    if occur := occurrences(target_file, target_byte):
        for line, col, _ in occur:
            print(
                f"{vscode_openable(target_file, line, col)}:",
                f"Found byte 0x{target_byte:02X}",
            )
    else:
        print(f"{target_file}: Byte 0x{target_byte:02X} not found.")
        return


if __name__ == "__main__":
    main()
