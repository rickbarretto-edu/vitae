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

import eliot

from src.features.ingestion import converter as convert
from src.features.ingestion import debug
from src.features.ingestion.log import log_into
from src.features.ingestion.parser import CurriculumParser
from src.features.ingestion.scanner import parallel_scanning, serial_scanning
from src.infra.database import Database
from src.lib.panic import panic

from . import converter, schema

__all__ = [
    "converter",
    "debug",
    "ingestion",
    "parallel_scanning",
    "schema",
    "serial_scanning",
]


def ingestion(database: Database) -> Callable[[Path], None]:
    """Process a directory containing XML files."""
    return lambda subdir: process_directory(database, subdir)


@eliot.log_call(action_type="scanning")
def process_directory(database: Database, directory: Path) -> None:
    """Process all curriculum files in a directory.

    Scans the given directory, processes each curriculum file using the parser,
    manages data buffers, and periodically flushes them to the database.
    """
    if not directory.exists():
        panic(f"Subdirectory does not exist: {directory}")

    logs: Path = Path("logs")

    for curriculum in directory.glob("*.xml"):
        parser = CurriculumParser(curriculum)

        researcher = log_into(parser.researcher(), logs / "researcher.log")
        model = convert.researcher_from(researcher)
        database.put.researcher(model)

        for experience in parser.experiences():
            log_into(experience, logs / "experience.log")
            model = convert.professional_experience_from(experience)
            database.put.experience(model)

        for background in parser.background():
            log_into(background, logs / "academic.log")
            model = convert.academic_background_from(background)
            database.put.academic_background(model)

        for area in parser.areas():
            log_into(area, logs / "area.log")
            model = convert.research_area_from(area)
            database.put.research_area(model)
