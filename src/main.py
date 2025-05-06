from src.pipeline_etl.extract.dir_scanning import directory_scanning
from src.database.database_creation import DatabaseCreation
from src.database.database_config import database_config

if __name__ == "__main__":
    database_creation = DatabaseCreation()
    database_config.run_migrations()
    directory_scanning.scanning()