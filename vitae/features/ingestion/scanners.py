"""Strategies to be used by the Ingestion Usecase."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Callable, Protocol

if TYPE_CHECKING:
    from collections.abc import Iterable

__all__ = ["Pool", "Scanner", "Serial"]


type FileParser = Callable[[Path], None]


class Scanner(Protocol):
    """Scanning Strategy Protocol."""

    scan_only: Iterable[Path] | None

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
