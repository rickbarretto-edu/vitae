"""Strategies to be used by the Ingestion Usecase."""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Callable, Protocol

from attr import dataclass

__all__ = ["Pool", "Scanner", "Serial"]


type FileParser = Callable[[Path], None]


class Scanner(Protocol):
    """Scanning Strategy Protocol."""

    def __call__(self, all_files: Path, parser: FileParser) -> None:
        """Scan `all_files` and parse with `parser`."""
        ...


@dataclass
class Serial:
    def __call__(self, all_files: Path, parser: FileParser) -> None:
        """Scan & Process files in order."""
        for directory in all_files.iterdir():
            parser(directory)


@dataclass
class Pool:
    max_workers: int = 8

    def __call__(self, all_files: Path, parser: FileParser) -> None:
        """Scan & Process files using Thread Pool (I/O bound)."""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for directory in all_files.iterdir():
                executor.submit(parser, directory)
