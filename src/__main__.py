from src.database.database_config import database_config
from src.database.database_creation import new_database
from src.parsing.scheduler import scan_directory
from src.utils.settings import vitae

if __name__ == "__main__":
    new_database(vitae)
    # TODO: DatabaseConfig should use Dependency Injection
    # Be careful with circular dependency.

    database_config.migrate()
    scan_directory(vitae.paths.curricula)
