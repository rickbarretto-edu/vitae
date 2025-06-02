from typing import TYPE_CHECKING

from sqlmodel import create_engine

from src import settings
from src.__setup__ import setup_database, setup_vitae
from src.features.database import Database
from src.features.ingestion.scanner import CurriculaScheduler

if TYPE_CHECKING:
    from sqlalchemy import Engine


def main() -> None:
    vitae: settings.VitaeSettings = settings.load()
    engine: Engine = create_engine(vitae.postgres.url, echo=True)

    setup_vitae(vitae)
    setup_database(vitae, engine)

    database = Database(engine)
    CurriculaScheduler(vitae, database).scan()


if __name__ == "__main__":
    main()
