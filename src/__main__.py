from src.__setup__ import new_vitae
from src.features.database import Database
from src.features.ingestion import debug
from src.features.ingestion.scanner import CurriculaScheduler
from src.settings import VitaeSettings


def main() -> VitaeSettings:
    vitae: VitaeSettings = new_vitae()

    database = Database(vitae.postgres.engine)
    CurriculaScheduler(vitae, database).scan()

    return vitae


if __name__ == "__main__":
    vitae = main()
    debug.display_first_20th_data(vitae)
