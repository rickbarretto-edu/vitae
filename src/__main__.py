from src.database.database_config import database_config
from src.database.database_creation import new_database
from src.pipeline_etl.extract.dir_scanning import scan_directory
from src.utils.settings import vitae

if __name__ == "__main__":
    new_database(vitae)
    database_config.migrate()
    scan_directory(vitae.paths.curricula)
