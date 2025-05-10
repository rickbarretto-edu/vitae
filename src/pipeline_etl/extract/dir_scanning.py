from concurrent.futures import ThreadPoolExecutor
import os

from src.pipeline_etl.extract.lattes_parser import parser
from src.utils.loggers import ConfigLogger

configLogger = ConfigLogger(__name__)
logger = configLogger.logger


class DirectoryScanning:
    """
    Class to scan the directory of Lattes curricula and search for all zipped curricula.
    """

    def __init__(self):
        pass

    def scanning(self):
        """
        SCANS THE DIRECTORY OF LATTES CURRICULA AND SEARCHES FOR ALL ZIPPED CURRICULA
        """
        try:
            current_directory = os.getcwd()
            logger.info(f"Current directory: {current_directory}")

            curriculum_directory = os.path.join(current_directory, "repo")
            if not os.path.exists(curriculum_directory):
                logger.error(
                    f"Curriculum directory does not exist: {curriculum_directory}"
                )
                return

            subdirectory_list = [
                os.path.join(curriculum_directory, sub)
                for sub in os.listdir(curriculum_directory)
                if os.path.isdir(os.path.join(curriculum_directory, sub))
            ]

            with ThreadPoolExecutor(max_workers=8) as executor:
                for subdirectory_path in subdirectory_list:
                    executor.submit(self.process_subdir, subdirectory_path)

            logger.info("Complete scan of all subdirectories.")
        except Exception as e:
            logger.error(f"An error occurred during the scan: {e}")


    def process_subdir(self, subdirectory):
        """
        Processes a single subdirectory containing curricula files.
        """
        if not os.path.exists(subdirectory):
            logger.warning(f"Subdirectory does not exist: {subdirectory}")
            return

        curricula = os.listdir(subdirectory)

        logger.info(
            f"Processing subdirectory: {subdirectory} with {len(curricula)} curricula"
        )

        general_data_buffer = []
        profession_buffer = []
        research_area_buffer = []
        education_buffer = []

        flush = False
        count = 0
        for curriculum in curricula:
            curriculum_path = os.path.join(subdirectory, curriculum)
            logger.debug(f"Opening curriculum: {curriculum_path}")

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

        logger.info(f"Subdirectory {subdirectory} processed successfully.")

        general_data_buffer.clear()
        profession_buffer.clear()
        research_area_buffer.clear()
        education_buffer.clear()


directory_scanning = DirectoryScanning()
