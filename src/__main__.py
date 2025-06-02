from src import settings
from src.__setup__ import setup_vitae
from src.features.database import Database
from src.features.ingestion.scanner import CurriculaScheduler


def main() -> None:
    vitae: settings.VitaeSettings = settings.load()

    setup_vitae(vitae)

    database = Database(vitae.postgres.engine)
    CurriculaScheduler(vitae, database).scan()


if __name__ == "__main__":
    main()
