from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Self

from src.features.ingestion.parser import CurriculumParser
from src.features.ingestion.repository import Researchers
from src.lib.panic import panic

__all__ = [
    "Ingestion",
]

type Scanner = Callable[[Path, Callable[[Path], None]], None]


@dataclass
class Ingestion:
    researchers: Researchers
    scanner: Scanner | None = None
    files: Path | None = None

    def using(
        self,
        scanner: Callable[[Path, Callable[[Path], None]], None],
        at: Path,
    ) -> Self:
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
        )
