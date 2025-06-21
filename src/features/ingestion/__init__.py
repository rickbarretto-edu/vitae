"""Ingestion package.

This package scan all XMLs files, parses it and
bring data to the system.

Usage
-----
    # For serial scanning ingestion
    serial_scanning(Path("all_files"), ingestion(database))

    # For parallel scanning ingestion
    arallel_scanning(Path("all_files"), ingestion(database))

"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

from src.features.ingestion import debug
from src.features.ingestion import scanners as strategy
from src.features.ingestion.parsing import CurriculumParser
from src.features.ingestion.repository import Researchers
from src.lib.panic import panic

__all__ = [
    "Ingestion",
    "Researchers",
    "debug",
    "processed_curricula_from",
    "strategy",
]


def processed_curricula_from(log: Path) -> set[str]:
    """Load all processed XML from logfile.

    Returns
    -------
    All processed Curricula's ID into a set.

    """
    with log.open("r") as file:
        result: set[str] = {line.strip("\n") + ".xml" for line in file}
    return result


@dataclass
class Ingestion:
    researchers: Researchers
    scanner: strategy.Scanner = strategy.serial
    files: Path | None = None
    to_skip: set[str] = field(default_factory=set)

    def using(self, scanner: strategy.Scanner, at: Path) -> Self:
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
