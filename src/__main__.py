from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine

from src.database.database_config import DatabaseConfig
from src.database.database_creation import new_database
from src.processing.commiter.commiter import UpsertService
from src.processing import CurriculaScheduler
from src.settings import vitae
from src.__setup__ import VitaeSetup


def start_database(engine: Engine):
    SQLModel.metadata.create_all(engine)


def main():
    engine = create_engine(vitae.postgres.url, echo=True)
    setup = VitaeSetup(vitae)
    database = DatabaseConfig()
    commiter = UpsertService(session=database.session, settings=vitae)

    setup.setup_logging()

    start_database(engine)
    CurriculaScheduler(vitae, commiter).scan()


if __name__ == "__main__":
    main()
