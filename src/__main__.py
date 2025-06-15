from pathlib import Path

from src.__setup__ import new_vitae
from src.features import ingestion as ingestions
from src.features.ingestion.usecases import Scanner
from src.infra.database import Database
from src.settings import VitaeSettings


def ingest(vitae: VitaeSettings, database: Database) -> None:
    """Ingest feature manager.

    Ingest data based on `vitae`'s settings into `database`.
    Curriculas are defined there.

    Notes
    -----
    - Use `scanners.serial` or `scanners.parallel` to define your strategy.
    - Define `buffer_limit` to define when a researcher
        will be properly commited to `database`.

    """
    buffer_limit: int = 50
    strategy: Scanner = ingestions.scanners.serial
    processed_log = Path("logs/ingestion/processed.log")

    researchers = ingestions.Researchers(db=database, every=buffer_limit)

    ingestion = ingestions.Ingestion(researchers)
    ingestion.using(strategy, at=vitae.paths.curricula).ingest(
        skip=ingestions.processed(processed_log),
    )


def main() -> VitaeSettings:
    vitae: VitaeSettings = new_vitae()
    database = Database(vitae.postgres.engine)

    ingest(vitae, database)

    return vitae


if __name__ == "__main__":
    vitae = main()
    ingestions.debug.display_first_20th_data(vitae)
