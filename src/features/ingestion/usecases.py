from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable, Protocol, Self

from src.features.ingestion import scanners as strategy
from src.features.ingestion.parser import CurriculumParser
from src.lib.panic import panic

if TYPE_CHECKING:
    from pathlib import Path

    from src.features.ingestion.repository import Researchers

__all__ = [
    "Ingestion",
]


class Scanner(Protocol):
    def __call__(self, all_files: Path, action: Callable[[Path], None]) -> None:
        pass


@dataclass
class Ingestion:
    researchers: Researchers
    scanner: Scanner = strategy.serial
    files: Path | None = None
    to_skip: set[str] = field(default_factory=set)

    def using(self, scanner: Scanner, at: Path) -> Self:
        """Add scanning strategy and file path."""  # noqa: DOC201
        self.scanner = scanner
        self.files = at
        return self

    def ingest(self, skip: set[str] | None = None) -> None:
        """Ingest data using the configured scanner and path.

        Raises
        ------
        RuntimeError:
            If scanner and files are not defined.

        """
        if skip is not None:
            self.to_skip = skip

        if self.scanner is None or self.files is None:
            msg = "Scanner function or file path not configured. Use `.using_at(...)` first."
            raise RuntimeError(msg)

        self.scanner(self.files, lambda x: self.process_directory(x))

    def process_directory(self, directory: Path) -> None:
        """Process all curriculum files in a directory.

        Scans the given directory, processes each curriculum file using the parser,
        manages data buffers, and periodically flushes them to the database.
        """
        if not directory.exists():
            panic(f"Subdirectory does not exist: {directory}")

        self.researchers.put(
            CurriculumParser(curriculum).all
            for curriculum in directory.glob("*.xml")
            if curriculum not in self.to_skip
        )
