"""Strategies to be used by the Ingestion Usecase."""

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Protocol

__all__ = ["Pool", "Scanner", "Serial"]


type FileParser = Callable[[Path], None]


class Scanner(Protocol):
    """Scanning Strategy Protocol."""

    def __call__(self, all_files: Path, parser: FileParser) -> None:
        """Scan `all_files` and parse with `parser`."""
        ...


@dataclass
class Serial:
    scan_only: set[str] = field(default_factory=set)

    def __call__(self, all_files: Path, parser: FileParser) -> None:
        """Scan & Process files in order."""
        (
            parser(directory)
            for directory in all_files.iterdir()
            if directory in self.scan_only
        )


@dataclass
class Pool:
    scan_only: set[str] = field(default_factory=set)
    max_workers: int = 8

    def __call__(self, all_files: Path, parser: FileParser) -> None:
        """Scan & Process files using Thread Pool (I/O bound)."""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            (
                executor.submit(parser, directory)
                for directory in all_files.iterdir()
                if directory in self.scan_only
            )
