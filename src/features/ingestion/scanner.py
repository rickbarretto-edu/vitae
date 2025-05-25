from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import eliot
from sqlalchemy import Engine

from src.database import Database
from src.lib.panic import panic
from src.processing.parsing import CurriculumParser
from src.settings import VitaeSettings

__all__ = ["CurriculaScheduler"]


class CurriculaScheduler:
    def __init__(self, vitae: VitaeSettings, engine: Engine):
        self._vitae: VitaeSettings = vitae
        self.engine = engine
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

        curricula = subdirectory.glob("*.xml")
        database = Database(self.engine)

        database.put.researchers(
            CurriculumParser(curriculum).researcher()
            for curriculum in curricula
        )

        database.put.experiences(
            experience
            for curriculum in curricula
            for experience in CurriculumParser(curriculum).experiences()
        )
