from typing import TYPE_CHECKING

from src.__setup__ import new_vitae, setup_vitae
from src.features.database import Database
from src.features.ingestion.scanner import CurriculaScheduler

if TYPE_CHECKING:
    from src.settings import VitaeSettings


def main() -> None:
    vitae: VitaeSettings = new_vitae()

    database = Database(vitae.postgres.engine)
    CurriculaScheduler(vitae, database).scan()


if __name__ == "__main__":
    main()
