from concurrent.futures import ThreadPoolExecutor
import os
from pathlib import Path

from src.pipeline_etl.extract.lattes_parser import parser
from src.utils.loggers import ConfigLogger

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

    try:

        # TODO: This should panic.
        if not curricula_folder.exists():
            message = "Curricula directory does not exist: %s"
            logger.error(message, curricula_folder)
            return
        
        # TODO: This should panic.
        if not curricula_folder.is_dir():
            message = "Curricula's path must be a directory: %s"
            logger.error(message, curricula_folder)
            return
        
        with ThreadPoolExecutor(max_workers=8) as executor:
            for subdirectory_path in curricula_folder.walk():
                executor.submit(process_subdir, subdirectory_path)

        logger.info("Complete scan of all subdirectories.")
    except Exception as e:
        logger.error("An error occurred during the scan: %s", e)


def process_subdir(subdirectory):
    """Process subdirectory.

    This function scans the specified subdirectory for curriculum files, processes
    each file using a parser, and manages data buffers for general data, professions,
    research areas, and education. It also handles periodic flushing of buffers to
    the database after processing a certain number of files.

    Parameters
    ----------
    subdirectory : str
        The path to the subdirectory containing curriculum files to be processed.

    Returns
    -------
    None
        This function does not return any value. It logs the processing status
        and manages data buffers internally.

    Notes
    -----
    - If the specified subdirectory does not exist, a warning is logged, and the
        function exits without processing.
    - Buffers are flushed to the database after every 50 files processed.
    - After processing all files in the subdirectory, the buffers are cleared.

    Logging
    -------
    - Logs a warning if the subdirectory does not exist.
    - Logs information about the number of curricula files being processed.
    - Logs debug information for each curriculum file being opened.
    - Logs when buffers are flushed to the database.
    - Logs a success message upon completing the processing of the subdirectory.

    Examples
    --------
    >>> process_subdir("/path/to/subdirectory")
    Processing subdirectory: /path/to/subdirectory with 10 curricula
    Flushing buffers to database.
    Subdirectory /path/to/subdirectory processed successfully.
    """

    if not os.path.exists(subdirectory):
        logger.warning("Subdirectory does not exist: %s", subdirectory)
        return

    curricula = os.listdir(subdirectory)

    logger.info(
        "Processing subdirectory: %s with %d curricula", subdirectory, len(curricula)
    )

    general_data_buffer = []
    profession_buffer = []
    research_area_buffer = []
    education_buffer = []

    flush = False
    count = 0
    for curriculum in curricula:
        curriculum_path = os.path.join(subdirectory, curriculum)
        logger.debug("Opening curriculum: %s", curriculum_path)

        if count == 50:
            flush = True
            logger.info("Flushing buffers to database.")

        parser.open_curriculum(
            curriculum_path,
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
