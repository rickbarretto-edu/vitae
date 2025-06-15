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

from pathlib import Path
from typing import Callable

from src.features.ingestion import debug
from src.features.ingestion.parser import CurriculumParser
from src.features.ingestion.repository import Researchers
from src.features.ingestion.scanner import parallel_scanning, serial_scanning
from src.lib.panic import panic

from . import schema

__all__ = [
    "debug",
    "ingestion",
    "parallel_scanning",
    "schema",
    "serial_scanning",
]


def ingestion(researchers: Researchers) -> Callable[[Path], None]:
    """Process a directory containing XML files."""
    return lambda subdir: process_directory(researchers, subdir)


def process_directory(researchers: Researchers, directory: Path) -> None:
    """Process all curriculum files in a directory.

    Scans the given directory, processes each curriculum file using the parser,
    manages data buffers, and periodically flushes them to the database.
    """
    if not directory.exists():
        panic(f"Subdirectory does not exist: {directory}")

    researchers.put(
        CurriculumParser(curriculum).all
        for curriculum in directory.glob("*.xml")
    )
