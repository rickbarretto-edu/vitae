from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from src.parsing.load import load
from src.parsing.parser import parser
from src.utils.loggers import ConfigLogger
from src.panic import panic

logger = ConfigLogger(__name__).logger

__all__ = ["scan_directory"]

@dataclass(kw_only=True)
class Buffer[T]:
    """Buffer stores data in batch and then flushes it when reaches it's maximum.

    This class is designed to encapsulate the batching and flushing logic, 
    reducing boilerplate code and avoiding primitive obsession. 

    Why not use lists and manual flushing?
    --------------------------------------
    Manually managing lists, counters, and flush flags across modules
    leads to scattered state and logic, making the code harder to maintain and reason about. 
    This approach increases the risk of bugs, such as forgetting to clear the list, 
    mishandling the flush condition, or introducing race conditions in concurrent scenarios.

    The older code used this approach, which is harder to reason about, 
    since the logic was distributed between two different modules with different purposes.    
    """

    data: list[T] = []
    max: int = 64
    on_flush: Callable[[list[T]], None] = lambda xs: None

    def push(self, value: T) -> Self:
        if len(self) >= self.max:
            self.on_flush(self.data)
            self.data.clear()

        self.data.append(value)
        return self

    def __len__(self) -> int:
        return len(self.data)


def scan_directory(curricula_folder: Path):
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
    if not curricula_folder.exists():
        panic(
            "Curricula directory does not exist: %s",
            curricula_folder,
            logger=logger,
        )

    if not curricula_folder.is_dir():
        panic(
            "Curricula's path must be a directory: %s",
            curricula_folder,
            logger=logger,
        )

    with ThreadPoolExecutor(max_workers=8) as executor:
        for folder, _, _ in curricula_folder.walk():
            executor.submit(process_subdir, folder)

    logger.info("Complete scan of all subdirectories.")


def process_subdir(subdirectory: Path):
    """Process all curriculum files in a subdirectory.

    Scans the given subdirectory, processes each curriculum file using the parser,
    manages data buffers, and periodically flushes them to the database.
    """

    if not subdirectory.exists():
        panic("Subdirectory does not exist: %s", subdirectory, logger=logger)

    logger.info("Processing subdirectory: %s", subdirectory)

    general_data_buffer = []
    profession_buffer = []
    research_area_buffer = []
    education_buffer = []

    count = 0
    for curriculum, _, _ in subdirectory.walk():
        parser.open_curriculum(
            curriculum,
            general_data_buffer,
            profession_buffer,
            research_area_buffer,
            education_buffer
        )
        count += 1

        if count % 10 == 0 and count > 10:
            logger.info("Flushing buffers to database.")

            load.upsert_researcher(general_data_buffer)
            load.upsert_professional_experience(profession_buffer)
            load.upsert_academic_background(education_buffer)
            load.upsert_research_area(research_area_buffer)

    logger.info("Subdirectory %s processed successfully.", subdirectory)

    general_data_buffer.clear()
    profession_buffer.clear()
    research_area_buffer.clear()
    education_buffer.clear()
