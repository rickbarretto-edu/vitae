"""Each use-case for Ingestion feature."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from vitae.features.ingestion.adapters import Curriculum
from vitae.features.ingestion.parsing import CurriculumParser
from vitae.lib.panic import panic

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path

    from vitae.features.ingestion import scanners as strategy
    from vitae.features.ingestion.repository import Researchers


@dataclass(kw_only=True)
class Ingestion:
    """Ingest documents to the database using Researchers's Repository."""

    researchers: Researchers
    files: Path
    scanner: strategy.Scanner

    scan_only: list[str] = field(default_factory=list)
    to_skip: set[str] = field(default_factory=set)
    workers: int = 8

    def ingest(self) -> None:
        """Ingest data using the configured scanner and path."""
        self.scanner(self.files, lambda x: self.process_directory(x))  # noqa: PLW0108

    def process_directory(self, directory: Path) -> None:
        """Process all curriculum files in a directory."""
        if not directory.exists():
            panic(f"Subdirectory does not exist: {directory}")

        self.researchers.put(cv for cv in self.all_curricula(directory))
        print(f"Processed {directory.parent.name}/{directory.name}")  # noqa: T201

    def all_curricula(self, directory: Path) -> Iterator[Curriculum]:
        """Iterate all curricula from `directory`.

        Yields
        ------
        Iterator of Curriculum.

        """
        for curriculum in directory.glob("*.xml"):
            if curriculum not in self.to_skip:
                parser = CurriculumParser(curriculum)
                cv = Curriculum(
                    researcher=parser.researcher,
                    address=parser.address,
                    education=list(parser.academic),
                    experience=list(parser.experience),
                )
                yield cv
