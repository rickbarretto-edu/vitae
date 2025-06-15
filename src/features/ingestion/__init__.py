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
from src.features.ingestion.scanner import parallel_scanning, serial_scanning
from src.infra.database import Database
from src.lib.panic import panic

from . import schema

__all__ = [
    "debug",
    "ingestion",
    "parallel_scanning",
    "schema",
    "serial_scanning",
]


def ingestion(database: Database) -> Callable[[Path], None]:
    """Process a directory containing XML files."""
    return lambda subdir: process_directory(database, subdir)


def process_directory(database: Database, directory: Path) -> None:
    """Process all curriculum files in a directory.

    Scans the given directory, processes each curriculum file using the parser,
    manages data buffers, and periodically flushes them to the database.
    """
    if not directory.exists():
        panic(f"Subdirectory does not exist: {directory}")

    for curriculum in directory.glob("*.xml"):
        ingest_curriculum(database, curriculum)


def ingest_curriculum(database: Database, curriculum_file: Path) -> None:
    curriculum = CurriculumParser(curriculum_file).all

    database.put.researcher(curriculum.personal_data)

    for experience in curriculum.professional_experiences:
        database.put.experience(experience)

    for background in curriculum.academic_background:
        database.put.academic_background(background)

    for area in curriculum.research_areas:
        database.put.research_area(area)
