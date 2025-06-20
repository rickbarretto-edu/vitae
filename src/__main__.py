from pathlib import Path

from src.__setup__ import new_vitae
from src.features import ingestion as ingestions
from src.features.ingestion.usecases import Scanner
from src.infra.database import Database
from src.settings import VitaeSettings


def ingest(
    vitae: VitaeSettings,
    database: Database,
    buffer_limit: int = 50,
    strategy: Scanner = ingestions.scanners.serial,
    processed_log: Path = Path("logs/ingestion/processed.log"),
) -> ingestions.Ingestion:
    """Ingest feature manager.

    Ingest data based on `vitae`'s settings into `database`.
    Curriculas are defined there.

    Returns
    -------
    A configured instance of Ingestion feature.

    Notes
    -----
    - Use `scanners.serial` or `scanners.parallel` to define your strategy.
    - Define `buffer_limit` to define when a researcher
        will be properly commited to `database`.

    """
    processed_xmls = ingestions.processed(processed_log)

    return ingestions.Ingestion(
        researchers=ingestions.Researchers(
            db=database,
            every=buffer_limit,
        ),
        scanner=strategy,
        files=vitae.paths.curricula,
        to_skip=processed_xmls,
    )


def main() -> VitaeSettings:
    vitae: VitaeSettings = new_vitae()
    database = Database(vitae.postgres.engine)

    ingestion = ingest(vitae, database, strategy=ingestions.scanners.parallel)
    ingestion.ingest()

    return vitae


if __name__ == "__main__":
    vitae = main()
    ingestions.debug.display_first_20th_data(vitae)
