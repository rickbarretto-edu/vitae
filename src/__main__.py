from loguru import logger

from src.database.database_config import DatabaseConfig
from src.database.database_creation import new_database
from src.processing.commiter.commiter import UpsertService
from src.processing import CurriculaScheduler
from src.settings import vitae
from src.__setup__ import VitaeSetup


def main():
    setup = VitaeSetup(vitae)
    database = DatabaseConfig()
    commiter = UpsertService(session=database.session, settings=vitae)
    scheduler = CurriculaScheduler(vitae, commiter)

    setup.setup_logging()

    logger.info("Session should connect to: {}", vitae.postgres.url)
    new_database(vitae)
    database.migrate()
    scheduler.scan()


if __name__ == "__main__":
    main()
