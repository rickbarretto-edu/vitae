from concurrent.futures import ThreadPoolExecutor
import os

from src.pipeline_etl.extract.lattes_parser import parser
from src.utils.loggers import ConfigLogger

configLogger = ConfigLogger(__name__)
logger = configLogger.logger

__all__ = ["scan_directory"]


def scan_directory():
    """
    SCANS THE DIRECTORY OF LATTES CURRICULA AND SEARCHES FOR ALL ZIPPED CURRICULA
    """
    try:
        current_directory = os.getcwd()
        logger.info("Current directory: %s", current_directory)

        curriculum_directory = os.path.join(current_directory, "repo")
        if not os.path.exists(curriculum_directory):
            logger.error(
                "Curriculum directory does not exist: %s", curriculum_directory
            )
            return

        subdirectory_list = [
            os.path.join(curriculum_directory, sub)
            for sub in os.listdir(curriculum_directory)
            if os.path.isdir(os.path.join(curriculum_directory, sub))
        ]

        with ThreadPoolExecutor(max_workers=8) as executor:
            for subdirectory_path in subdirectory_list:
                executor.submit(process_subdir, subdirectory_path)

        logger.info("Complete scan of all subdirectories.")
    except Exception as e:
        logger.error("An error occurred during the scan: %s", e)


def process_subdir(subdirectory):
    """
    Processes a single subdirectory containing curricula files.
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
