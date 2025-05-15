from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from src.parsing.parser import parser
from src.utils.loggers import ConfigLogger
from src.panic import panic

logger = ConfigLogger(__name__).logger

__all__ = ["scan_directory"]


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

    flush = False
    count = 0
    for curriculum, _, _ in subdirectory.walk():
        if count % 10 == 0 and count > 10:
            flush = True
            logger.info("Flushing buffers to database.")

        parser.open_curriculum(
            curriculum,
            general_data_buffer,
            profession_buffer,
            research_area_buffer,
            education_buffer,
            flush,
        )
        count += 1

    logger.info("Subdirectory %s processed successfully.", subdirectory)

    general_data_buffer.clear()
    profession_buffer.clear()
    research_area_buffer.clear()
    education_buffer.clear()
