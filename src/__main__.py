from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine

# Loads models to register them in SQLModel
from src import models as models

from src.processing.commiter.commiter import UpsertService
from src.processing import CurriculaScheduler
from src.settings import vitae
from src.__setup__ import VitaeSetup


def start_database(engine: Engine):
    SQLModel.metadata.create_all(engine)


def main():
    engine = create_engine(vitae.postgres.url, echo=True)
    setup = VitaeSetup(vitae)
    commiter = UpsertService(engine)

    setup.setup_logging()

    start_database(engine)
    CurriculaScheduler(vitae, commiter).scan()


if __name__ == "__main__":
    main()
