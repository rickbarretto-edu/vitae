import os
from src.pipeline_etl.extract.lattes_parser import parser
from src.utils.loggers import ConfigLogger
from concurrent.futures import ThreadPoolExecutor

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
            currentDirectory = os.getcwd()
            logger.info(f"Current directory: {currentDirectory}")

            curriculumDirectory = os.path.join(currentDirectory, "repo")
            if not os.path.exists(curriculumDirectory):
                logger.error(f"Curriculum directory does not exist: {curriculumDirectory}")
                return
            
            subdirectoryList = [os.path.join(curriculumDirectory, sub) for sub in os.listdir(curriculumDirectory) if os.path.isdir(os.path.join(curriculumDirectory, sub))]

            with ThreadPoolExecutor(max_workers=8) as executor:
                for subdirectoryPath in subdirectoryList:
                    executor.submit(self.processSubDir, subdirectoryPath)
                    
            logger.info("Complete scan of all subdirectories.")
        except Exception as e:
            logger.error(f"An error occurred during the scan: {e}")

    def processSubDir(self, subdirectory):
        """
        Processes a single subdirectory containing curricula files.
        """
        if not os.path.exists(subdirectory):
            logger.warning(f"Subdirectory does not exist: {subdirectory}")
            return
        
        curricula = os.listdir(subdirectory)
        
        logger.info(f"Processing subdirectory: {subdirectory} with {len(curricula)} curricula")

        generalDataBuffer = []
        professionBuffer = []
        researchAreaBuffer = []
        educationBuffer = []
        
        flush = False  
        count = 0  
        for curriculum in curricula:

            curriculumPath = os.path.join(subdirectory, curriculum)
            logger.debug(f"Opening curriculum: {curriculumPath}")

            if count == 50:
                flush = True
                logger.info("Flushing buffers to database.")

            parser.openCurriculum(curriculumPath, generalDataBuffer, professionBuffer, researchAreaBuffer, educationBuffer, flush)
            count += 1

        logger.info(f"Subdirectory {subdirectory} processed successfully.")
        
        generalDataBuffer.clear()
        professionBuffer.clear()
        researchAreaBuffer.clear()
        educationBuffer.clear()

directory_scanning = DirectoryScanning()