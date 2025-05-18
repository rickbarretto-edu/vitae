from src.database.database_config import database_config
from src.database.database_creation import new_database
from src.processing import CurriculaScheduler
from src.settings import vitae
from src.__setup__ import VitaeSetup

setup = VitaeSetup(vitae)


if __name__ == "__main__":
    setup.setup_logging()

    new_database(vitae)
    # TODO: DatabaseConfig should use Dependency Injection
    # Be careful with circular dependency.

    database_config.migrate()
    CurriculaScheduler(vitae).scan()
