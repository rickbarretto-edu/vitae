from pathlib import Path
from typing import Literal

import cyclopts

from src.shared import database, vitae

from . import scanners
from .repository import Researchers
from .usecase import Ingestion

__all__ = ["app"]

app = cyclopts.App(name="ingest", help="Ingest XML documents into database.")


@app.command
def ingest(
    sub_folders: list[int] | None = None,
    strategy: Literal["serial", "pool"] = "pool",
    buffer_limit: int = 50,
    processed_log: Path = Path("logs/ingestion/processed.log"),
) -> None:
    repository = Researchers(db=database, every=buffer_limit)
    scanner = {
        "serial": scanners.serial,
        "pool": scanners.thread_pool,
    }[strategy]
    processed_curricula = curricula_xml_from(processed_log)

    ingestion = Ingestion(
        researchers=repository,
        scanner=scanner,
        files=vitae.paths.curricula,
        to_skip=processed_curricula,
    )

    ingestion.ingest()


# =~=~=~=~=~=~ Helper Functions ~=~=~=~=~=~=


def curricula_xml_from(log: Path) -> set[str]:
    """Load curricula from log file.

    Note:
    ----
    Its expected that each line contains only one Researcher's ID.

    Returns:
    -------
    All processed Curricula's ID into a set as `<id>.xml` strings.

    """
    with log.open("r") as file:
        result: set[str] = {line.strip("\n") + ".xml" for line in file}
    return result
