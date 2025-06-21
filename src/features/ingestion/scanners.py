"""Strategies to be used by the Ingestion Usecase."""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Callable, Protocol

__all__ = ["Scanner", "parallel", "serial"]


type FileParser = Callable[[Path], None]


class Scanner(Protocol):
    def __call__(self, all_files: Path, action: FileParser) -> None:
        pass


def serial(all_files: Path, action: FileParser) -> None:
    """Scan & Process files in order."""
    for directory in all_files.iterdir():
        action(directory)


def parallel(all_files: Path, action: FileParser) -> None:
    """Scan & Process files in parallel (I/O bound)."""
    with ThreadPoolExecutor(max_workers=8) as executor:
        for directory in all_files.iterdir():
            executor.submit(action, directory)
