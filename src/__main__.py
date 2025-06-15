from src.__setup__ import new_vitae
from src.features.ingestion import Ingestion, debug, serial_scanning
from src.features.ingestion.repository import Researchers
from src.infra.database import Database
from src.settings import VitaeSettings


def main() -> VitaeSettings:
    vitae: VitaeSettings = new_vitae()
    database = Database(vitae.postgres.engine)
    researchers = Researchers(db=database, every=50)

    serial_scanning(
        vitae.paths.curricula,
        Ingestion(researchers).new(),
    )

    return vitae


if __name__ == "__main__":
    vitae = main()
    debug.display_first_20th_data(vitae)
