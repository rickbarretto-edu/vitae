"""Strategies to be used by the Ingestion Usecase."""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Callable, Protocol

__all__ = ["Scanner", "parallel", "serial"]

class Scanner(Protocol):
    def __call__(self, all_files: Path, action: Callable[[Path], None]) -> None:
        pass


def serial(
    all_files: Path,
    action: Callable[[Path], None],
) -> None:
    """Scan & Process files in order."""
    for directory in all_files.iterdir():
        action(directory)


def parallel(
    all_files: Path,
    action: Callable[[Path], None],
) -> None:
    """Scan & Process files in parallel (I/O bound)."""
    with ThreadPoolExecutor(max_workers=8) as executor:
        for directory in all_files.iterdir():
            executor.submit(action, directory)
