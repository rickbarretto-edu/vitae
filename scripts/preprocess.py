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
from functools import wraps
from pathlib import Path
import sys
import time
from typing import Protocol, Self
from xml.dom.minidom import parseString as XmlDom
from zipfile import ZipFile


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
            result = func(self, *args, **kwargs)
            print(message.format(self.file))
            return result

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

    def __bool__(self) -> bool:
        return self.file.exists()

    @log("TO UTF-8 >> {}")
    def to_utf_8(self) -> "Xml":
        output = "utf-8"
        content = self.file.read_text(encoding=self.encoding)
        self.file.write_text(content, encoding=output)

        return Xml(self.file, "utf-8")

    @log("PRETTIFY >> {}")
    def prettify(self) -> "Xml":
        content = self.file.read_text(encoding=self.encoding)
        self.file.write_text(
            XmlDom(content).toprettyxml(indent="  "),
            encoding=self.encoding,
        )

        return self


@dataclass
class Zip:
    file: Path

    def __post_init__(self):
        assert self.file.exists()
        assert self.file.is_file()
        assert self.file.name.endswith(".zip")

    @log("UNZIP >> {}")
    def unzip(self) -> Self:
        ZipFile(self.file, "r").extractall(self.file.parent)
        return self

    def xml(self) -> Xml:
        filename = self.file.name.removesuffix(".zip")
        return Xml(self.file.parent / f"{filename}.xml")

    @log("UNLINK >> {}...")
    def unlink(self) -> None:
        self.file.unlink()


def optmized(all_files: Path) -> None:
    """Script entry

    Preprocess all files, skipping the already pre-processed.

    Be careful. Since we can't ensure the file was already converted to UTF-8,
    this script only seeks if the equvalente XML file exists.
    """
    count: int = 0
    skipped: int = 0
    start = time.time()

    for count, archive in enumerate(all_files.glob("**/*.zip"), start=1):
        archive = Zip(archive)
        extracted = archive.xml()

        if not extracted:
            archive.unzip()
            extracted.to_utf_8().prettify()
            print()
        else:
            skipped += 1

    print(
        f"[FINISHED] {count} files processed, {skipped} skipped. In {time.time() - start} seconds.",
    )


def force(all_files: Path, sub_folders: list[str]) -> None:
    """Script Entry

    Pre-process all files inside the passed sub-directory.
    Pass each sub-directory you want to force the processing.
    """
    count: int = 0
    start = time.time()

    for sub_folder in sub_folders:
        for archive in all_files.glob(f"{sub_folder}/**/*.zip"):
            Zip(archive).unzip().xml().to_utf_8().prettify()
            count += 1

            print()

    print(
        f"[FINISHED] {count} files forcedly processed in {time.time() - start} seconds",
    )


def cli() -> None:
    """Script entry

    Preprocess all files, skipping the already pre-processed ones.
    To force pre-process, pass --force <sub-dirs>.

    Use the `tee` command (Unix and DOS) to log the output.

    Usage
    -----
        $ poetry run pre-process | tee logs/pre-processing.log

        # Forced pre-process of directories 01 and 02
        # This also softly pre-process all the rest
        $ poetry run pre-process --force 01 02 | tee logs/pre-processing.log
    """
    assert len(sys.argv) >= 2

    all_files = Path(sys.argv[1])

    if len(sys.argv) >= 4:
        if sys.argv[2] == "--force":
            force(all_files, sys.argv[2:])

    optmized(all_files)
    print()
