from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from src.features.ingestion.parser import CurriculumParser
from src.features.ingestion.repository import Researchers
from src.lib.panic import panic

__all__ = [
    "Ingestion",
]


@dataclass
class Ingestion:
    researchers: Researchers

    def new(self) -> Callable[[Path], None]:
        """Process a directory containing XML files.

        Returns
        -------
        Ingestion function needed by scan.

        """

        def fn(subdir: Path) -> None:
            self.process_directory(subdir)

        return fn

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
