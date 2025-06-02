from sqlalchemy import Engine
from sqlmodel import SQLModel, create_engine

# Loads models to register them in SQLModel
from src import models as models  # noqa: PLC0414
from src import settings
from src.__setup__ import setup_vitae
from src.features.database import Database
from src.features.ingestion.scanner import CurriculaScheduler


def start_database(vitae: settings.VitaeSettings, engine: Engine) -> None:
    if vitae.in_development:
        SQLModel.metadata.drop_all(engine)

    SQLModel.metadata.create_all(engine)


def main() -> None:
    vitae: settings.VitaeSettings = settings.load()
    engine: Engine = create_engine(vitae.postgres.url, echo=True)

    setup_vitae(vitae)
    start_database(vitae, engine)

    database = Database(engine)
    CurriculaScheduler(vitae, database).scan()


if __name__ == "__main__":
    main()
