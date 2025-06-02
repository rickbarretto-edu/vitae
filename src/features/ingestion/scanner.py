"""Curricula directory scanner."""

from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Callable

import eliot

from src.features.database import Database
from src.features.ingestion.log import log_into
from src.lib.panic import panic
from src.settings import VitaeSettings

from . import converter as convert
from .parser import CurriculumParser

if TYPE_CHECKING:
    from collections.abc import Iterator

__all__ = ["CurriculaScheduler"]


@dataclass
class CurriculaScheduler:
    """Scan directories and schedules parsing."""

    vitae: VitaeSettings
    database: Database

    def __post_init__(self) -> None:
        """Initialize curricula_folder and check if this is valid."""
        self.curricula_folder: Path = Path(self.vitae.paths.curricula)

        if not self.curricula_folder.exists():
            msg = f"Curricula folder must exist: {self.curricula_folder}"
            panic(msg)

        if not self.curricula_folder.is_dir():
            msg = f"Curricula path must be a directory: {self.curricula_folder}"
            panic(msg)

    @eliot.log_call(action_type="scanning")
    def scan(self) -> None:
        """Scan the directory curricula and process all subdirectories.

        This function identifies the current working directory,
        verifies the existence of a "repo" directory containing subdirectories
        of curricula, and processes each subdirectory concurrently
        using a thread pool.

        Each subdirectory is expected to contain zipped curricula files,
        which are parsed and processed.

        Notes
        -----
        - The function logs the progress and any errors encountered
          during execution.
        - Subdirectories are processed in parallel to improve performance.

        """
        sub_directories = self.curricula_folder.iterdir()

        if self.vitae.in_development:
            serial_scanning(
                sub_directories,
                lambda files: process_directory(self.database, files),
            )
        else:
            parallel_scanning(
                sub_directories,
                lambda files: process_directory(self.database, files),
            )


def serial_scanning(
    directories: Iterable[Path],
    action: Callable[[Path], None],
) -> None:
    for directory in directories:
        action(directory)


def parallel_scanning(
    directories: Iterable[Path],
    action: Callable[[Path], None],
) -> None:
    with ThreadPoolExecutor(max_workers=8) as executor:
        for directory in directories:
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
