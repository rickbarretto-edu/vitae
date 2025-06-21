from pathlib import Path
from typing import Literal

import cyclopts

from src.features.ingestion import (
    Ingestion,
    Researchers,
    curricula_xml_from,
    scanners,
)
from src.shared import database, vitae

app = cyclopts.App()


@app.command
def ingestion(
    sub_folders: list[int] | None = None,
    strategy: Literal["serial", "pool"] = "serial",
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
