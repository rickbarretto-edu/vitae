"""Each use-case for Ingestion feature."""

from __future__ import annotations

from collections.abc import Generator
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from vitae.features.ingestion.adapters import Curriculum
from vitae.features.ingestion.parsing import CurriculumDocument
from vitae.lib.panic import panic

if TYPE_CHECKING:
    from pathlib import Path

    from vitae.features.ingestion.repository import Researchers


@dataclass(kw_only=True)
class Ingestion:
    """Ingest documents to the database using Researchers's Repository."""

    researchers: Researchers
    files: Path

    scan_only: frozenset[Path] | None = field(default_factory=frozenset)
    to_skip: set[str] = field(default_factory=set)

    def ingest(self) -> None:
        """Ingest data using the configured path and filter."""
        for id_group in self.files.iterdir():
            if (not self.scan_only) or id_group in self.scan_only:
                self.process_group(id_group)

    def process_group(self, directory: Path) -> None:
        """Process all curriculum files in a directory."""
        if not directory.exists():
            panic(f"Subdirectory does not exist: {directory}")

        self.researchers.put(process_each(directory, self.to_skip))
        print(f"Processed {directory.parent.name}/{directory.name}")


def process_each(
    directory: Path, to_skip: set) -> Generator[Curriculum, Any, None]:
    for curriculum in directory.glob("*.xml"):
        if curriculum.name not in to_skip:
            yield CurriculumDocument(curriculum).as_schema
        else:
            print(f"Skipping: {curriculum}")
