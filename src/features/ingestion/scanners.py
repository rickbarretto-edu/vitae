"""Strategies to be used by the Ingestion Usecase."""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Callable, Protocol

__all__ = ["Scanner", "serial", "thread_pool"]


type FileParser = Callable[[Path], None]


class Scanner(Protocol):
    """Scanning Strategy Protocol.

    All Scanning strategies must follow this Protocol.
    """

    def __call__(self, all_files: Path, action: FileParser) -> None:
        """All scanners follows this pattern.

        You can define your scanner as a raw function:

        Example:
        -------
            def scanner(all_files: Path, action: FileParser) -> None:
                ...

        """


def serial(all_files: Path, action: FileParser) -> None:
    """Scan & Process files in order."""
    for directory in all_files.iterdir():
        action(directory)


def thread_pool(all_files: Path, action: FileParser) -> None:
    """Scan & Process files using Thread Pool (I/O bound)."""
    with ThreadPoolExecutor(max_workers=8) as executor:
        for directory in all_files.iterdir():
            executor.submit(action, directory)
