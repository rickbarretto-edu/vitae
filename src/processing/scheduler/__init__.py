from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import eliot
from loguru import logger

from src.lib.panic import panic
from src.lib.buffer import Buffer
from src.processing.buffers import CurriculaBuffer
from src.processing.commiter import load
from src.processing.parsing import CurriculumParser
from src.settings import VitaeSettings

__all__ = ["CurriculaScheduler"]


class CurriculaScheduler:
    def __init__(self, vitae: VitaeSettings):
        self._vitae: VitaeSettings = vitae
        self._curricula_folder: Path = Path(self._vitae.paths.curricula)

        if not self._curricula_folder.exists():
            panic(f"Curricula folder does not exist: {self._curricula_folder}")
        if not self._curricula_folder.is_dir():
            panic(
                f"Curricula path is not a directory: {self._curricula_folder}"
            )

    @eliot.log_call(action_type="scanning")
    def scan(self):
        """
        Scan the directory containing Lattes curricula and process all subdirectories.

        This function identifies the current working directory, verifies the existence
        of a "repo" directory containing subdirectories of curricula, and processes
        each subdirectory concurrently using a thread pool. Each subdirectory is expected
        to contain zipped curricula files, which are parsed and processed.

        Raises
        ------
        Exception
            If an error occurs during the scanning or processing of directories.

        Notes
        -----
        - The function logs the progress and any errors encountered during execution.
        - Subdirectories are processed in parallel to improve performance.
        """
        if self._vitae.in_development:
            self._serial_execution()
        else:
            self._parallel_execution()

    def _serial_execution(self):
        for folder in self._curricula_folder.iterdir():
            self._process_subdir(folder)

    def _parallel_execution(self):
        with ThreadPoolExecutor(max_workers=8) as executor:
            for folder in self._curricula_folder.iterdir():
                executor.submit(self._process_subdir, folder)

    @eliot.log_call(action_type="scanning")
    def _process_subdir(self, subdirectory: Path):
        """Process all curriculum files in a subdirectory.

        Scans the given subdirectory, processes each curriculum file using the parser,
        manages data buffers, and periodically flushes them to the database.
        """

        if not subdirectory.exists():
            panic(f"Subdirectory does not exist: {subdirectory}")

        for curriculum in subdirectory.glob("*.xml"):
            self._process_curriculum(curriculum)

    @eliot.log_call(action_type="scanning")
    def _process_curriculum(self, curriculum: Path):
        def buffer(action) -> Buffer:
            max: int = self._vitae.postgres.db.flush_every
            return (
                Buffer(max=max)
                .on_flush(action)
                .then(lambda xs: logger.info("Flushed {} items", len(xs)))
            )

        buffers = CurriculaBuffer(
            general=buffer(load.upsert_researcher),
            professions=buffer(load.upsert_professional_experience),
            research_areas=buffer(load.upsert_academic_background),
            educations=buffer(load.upsert_research_area),
        )

        CurriculumParser(curriculum, buffers).parse()
