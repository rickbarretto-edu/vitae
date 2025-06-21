"""Each use-case for Ingestion feature."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Self

from src.features.ingestion import scanners as strategy
from src.features.ingestion.parsing import CurriculumParser
from src.lib.panic import panic

if TYPE_CHECKING:
    from pathlib import Path

    from src.features.ingestion.repository import Researchers


@dataclass
class Ingestion:
    """Ingest documents to the database using Researchers's Repository."""

    researchers: Researchers
    scanner: strategy.Scanner = strategy.serial
    files: Path | None = None
    to_skip: set[str] = field(default_factory=set)

    def using(self, scanner: strategy.Scanner, at: Path) -> Self:
        """Add scanning strategy and file path."""  # noqa: DOC201
        self.scanner = scanner
        self.files = at
        return self

    def ingest(self) -> None:
        """Ingest data using the configured scanner and path.

        Raises
        ------
        RuntimeError:
            If scanner and files are not defined.

        """
        if self.scanner is None or self.files is None:
            msg = "Scanner strategy or file path not configured."
            raise RuntimeError(msg)

        self.scanner(self.files, lambda x: self.process_directory(x))  # noqa: PLW0108

    def process_directory(self, directory: Path) -> None:
        """Process all curriculum files in a directory."""
        if not directory.exists():
            panic(f"Subdirectory does not exist: {directory}")

        self.researchers.put(
            CurriculumParser(curriculum).all
            for curriculum in directory.glob("*.xml")
            if curriculum not in self.to_skip
        )
