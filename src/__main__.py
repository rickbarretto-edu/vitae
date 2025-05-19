from sqlalchemy import text

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

    setup.setup_logging()

    new_database(vitae)
    database.migrate()
    CurriculaScheduler(vitae, commiter).scan()


def test_connection():
    session = DatabaseConfig().session
    session.execute(
        text("INSERT INTO researcher (id, name) VALUES ('test_id', 'Test Name')")
    )
    session.commit()


if __name__ == "__main__":
    # test_connection()
    main()
