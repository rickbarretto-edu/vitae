"""Curricula directory scanner.

Usage
-----

    def ingestion(database: Database) -> Callable[[Path], None]:
        return lambda sub: process_directory(database, sub)

    serial_scanning(Path("all_files"), ingestion(database))
    arallel_scanning(Path("all_files"), ingestion(database))

"""

from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import TYPE_CHECKING, Callable

import eliot

from src.features.database import Database
from src.features.ingestion.log import log_into
from src.lib.panic import panic

from . import converter as convert
from .parser import CurriculumParser

if TYPE_CHECKING:
    from collections.abc import Iterator

__all__ = ["parallel_scanning", "process_directory", "serial_scanning"]


def serial_scanning(
    all_files: Path,
    action: Callable[[Path], None],
) -> None:
    """Scan & Process files in order.

    Usage
    -----
        serial_scanning(path, lambda sub: process_directory(database, sub)
    """
    for directory in all_files.iterdir():
        action(directory)


def parallel_scanning(
    all_files: Path,
    action: Callable[[Path], None],
) -> None:
    """Scan & Process files in parallel (I/O bound).

    Usage
    -----
        parallel_scanning(path, lambda sub: process_directory(database, sub)

    """
    with ThreadPoolExecutor(max_workers=8) as executor:
        for directory in all_files.iterdir():
            executor.submit(action, directory)


@eliot.log_call(action_type="scanning")
def process_directory(database: Database, directory: Path) -> None:
    """Process all curriculum files in a directory.

    Scans the given directory, processes each curriculum file using the parser,
    manages data buffers, and periodically flushes them to the database.
    """
    if not directory.exists():
        panic(f"Subdirectory does not exist: {directory}")

    logs: Path = Path("logs")
    curricula: Iterator[Path] = directory.glob("*.xml")

    researcher_log: Path = logs / "researcher.log"
    experience_log: Path = logs / "experience.log"
    academic_log: Path = logs / "academic.log"
    area_log: Path = logs / "area.log"

    for curriculum in curricula:
        parser = CurriculumParser(curriculum)

        researcher = log_into(parser.researcher(), researcher_log)
        model = convert.researcher_from(researcher)
        database.put.researcher(model)

        for experience in parser.experiences():
            log_into(experience, experience_log)
            model = convert.professional_experience_from(experience)
            database.put.experience(model)

        for background in parser.background():
            log_into(background, academic_log)
            model = convert.academic_background_from(background)
            database.put.academic_background(model)

        for area in parser.areas():
            log_into(area, area_log)
            model = convert.research_area_from(area)
            database.put.research_area(model)
