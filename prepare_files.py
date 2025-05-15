"""This script is designed to pre-process all files before actually pushing it into PostgreSQL.

Data Processing Steps
---------------------

- Unzip all ``.zip`` files under `all_files`.
  - This make easier to parse the files by removing the unzip step before hand.
- Decode XML from ISO 8859-1 to UTF-8 due to compatibility issues with PostreSQL.
- Prettify XML files to make it easier to debug and inspect.
- Removes all old .zip files to save disk space.
"""

from dataclasses import dataclass
from typing import Protocol
from zipfile import ZipFile
from pathlib import Path
from functools import wraps
from xml.dom.minidom import parseString as XmlDom


class File(Protocol):
    file: Path


def log(message: str):
    """Logs action for certain `File`.

    Into your message, `{}` means the filename of `File`.

    Examples
    --------
    >>> @log("Processing file: {}")
    ... def process(self):
    ...     pass
    """

    def decorator(func):
        @wraps(func)
        def wrapper(self: File, *args, **kwargs):
            print(message.format(self.file.name))
            return func(self, *args, **kwargs)

        return wrapper

    return decorator


@dataclass
class Encoding:
    name: str
    pretty: str

    def __str__(self) -> str:
        return self.name


@dataclass
class Xml:
    file: Path

    encoding: str = "iso-8859-1"

    def __post_init__(self):
        assert self.file.exists()
        assert self.file.is_file()
        assert self.file.name.endswith(".xml")

    @log("converting {} to UTF-8")
    def to_utf_8(self) -> "Xml":
        output = "utf-8"
        content = self.file.read_text(encoding=self.encoding)
        self.file.write_text(content, encoding=output)

        return Xml(self.file, "utf-8")

    @log("Making {} readable...")
    def prettify(self) -> "Xml":
        content = self.file.read_text(encoding=self.encoding)
        self.file.write_text(
            XmlDom(content).toprettyxml(indent="  "), encoding=self.encoding
        )

        return self


@dataclass
class Zip:
    file: Path

    def __post_init__(self):
        assert self.file.exists()
        assert self.file.is_file()
        assert self.file.name.endswith(".zip")

    @log("Unzipping {}...")
    def unzip(self) -> "Zip":
        ZipFile(self.file, "r").extractall(self.file.parent)
        return self

    def xml(self) -> Xml:
        filename = self.file.name.removesuffix(".zip")
        return Xml(self.file.parent / f"{filename}.xml")

    @log("Unliking {}...")
    def unlink(self) -> None:
        self.file.unlink()


if __name__ == "__main__":
    all_archives = Path("all_files").glob("**/*.zip")

    for archive in all_archives:
        archive = Zip(archive).unzip()

        extracted = archive.xml()

        extracted.to_utf_8().prettify()
        # TODO: ask for this
        # archive.unlink()

        print()
