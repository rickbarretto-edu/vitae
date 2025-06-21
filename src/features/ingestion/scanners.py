"""Strategies to be used by the Ingestion Usecase."""

from __future__ import annotations

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
    scan_only: Iterable[Path] | None = None

    def __call__(self, all_files: Path, parser: FileParser) -> None:
        """Scan & Process files in order."""
        for directory in all_files.iterdir():
            if self.scan_only is None or directory in self.scan_only:
                parser(directory)


@dataclass
class Pool:
    scan_only: Iterable[Path] | None = None
    max_workers: int = 8

    def __call__(self, all_files: Path, parser: FileParser) -> None:
        """Scan & Process files using Thread Pool (I/O bound)."""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for directory in all_files.iterdir():
                if self.scan_only is None or directory in self.scan_only:
                    executor.submit(parser, directory)
