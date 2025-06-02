"""Curricula directory scanner."""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Callable

__all__ = ["parallel_scanning", "serial_scanning"]


def serial_scanning(
    all_files: Path,
    action: Callable[[Path], None],
) -> None:
    """Scan & Process files in order."""
    for directory in all_files.iterdir():
        action(directory)


def parallel_scanning(
    all_files: Path,
    action: Callable[[Path], None],
) -> None:
    """Scan & Process files in parallel (I/O bound)."""
    with ThreadPoolExecutor(max_workers=8) as executor:
        for directory in all_files.iterdir():
            executor.submit(action, directory)
