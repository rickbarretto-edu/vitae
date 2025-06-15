from src.__setup__ import new_vitae
from src.features import ingestion as ingestions
from src.infra.database import Database
from src.settings import VitaeSettings


def ingest(vitae: VitaeSettings, database: Database):
    researchers = ingestions.Researchers(db=database, every=50)

    ingestion = ingestions.Ingestion(researchers)
    ingestion.using(
        ingestions.scanners.serial,
        at=vitae.paths.curricula,
    ).ingest()


def main() -> VitaeSettings:
    vitae: VitaeSettings = new_vitae()
    database = Database(vitae.postgres.engine)

    ingest(vitae, database)

    return vitae


if __name__ == "__main__":
    vitae = main()
    ingestions.debug.display_first_20th_data(vitae)
