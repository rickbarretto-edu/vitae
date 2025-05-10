from src.database.database_config import database_config
from src.database.database_creation import new_database
from src.pipeline_etl.extract.dir_scanning import directory_scanning

if __name__ == "__main__":
    new_database()
    database_config.migrate()
    directory_scanning.scanning()
