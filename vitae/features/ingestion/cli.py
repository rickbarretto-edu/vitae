from pathlib import Path
from typing import Annotated

import cyclopts
from cyclopts import Parameter

from vitae.infra.database import Database
from vitae.infra.database.settings import setup_database
from vitae.settings.logging import create_logs, erase_logs, redirect_loguru_to
from vitae.settings.vitae import Vitae

from .repository import Researchers
from .usecase import Ingestion

__all__ = ["app", "ingest"]

app = cyclopts.App(name="ingest")

type Indexes = frozenset[int]
type SelectedIndexes = list[int] | None
type IndexRange = tuple[int, int] | None
type Directories = frozenset[Path]


@app.default
def ingest(
    indexes: Annotated[
        list[int] | None,  # noqa: FA102
        Parameter(name=["--indexes", "-i"]),
    ] = None,
    _range: Annotated[IndexRange, Parameter(name=["--range", "-r"])] = None,
    buffer: Annotated[int, Parameter(name=["--buffer", "-b"])] = 50,
) -> None:
    """Ingest XML documents into the database.

    Parameters
    ----------
    indexes : list[int] | None = None
        Indicate which sub-directories should be scanned.
        If empty, scans all sub-directories.

    _range : tuple[int, int] | None = None
        Indicate the range of sub-directories to be scanned.
        Similar to `--only` and also can be combined.

    buffer : int, default=50
        Number of researchers to buffer before committing to the database.
        Use higher numbers on production.

    """
    vitae = Vitae.from_toml(Path("vitae.toml"))
    setup(vitae)
    database = Database(vitae.postgres.engine)

    root_directory = vitae.paths.curricula
    scan_only = merge_indexes(root_directory, indexes, _range)
    repository = Researchers(db=database, every=buffer)
    processed_curricula = curricula_xml_from(
        Path("logs/ingestion/processed.log"),
    )

    ingestion = Ingestion(
        researchers=repository,
        files=root_directory,
        to_skip=processed_curricula,
        scan_only=scan_only,
    )

    ingestion.ingest()


# =~=~=~=~=~=~ Helper Functions ~=~=~=~=~=~=


def merge_indexes(
    root_path: Path,
    selected: SelectedIndexes,
    rng: IndexRange,
) -> Directories | None:  # noqa: FA102
    """Merge manually selected with ranged selected indexes into a single one.

    Returns
    -------
    A set of directories's Path or Nothing.

    """

    def merge(selected: SelectedIndexes, rng: IndexRange) -> Indexes:
        selected_set = frozenset(selected) if selected else frozenset()
        range_set = frozenset(range(rng[0], rng[1] + 1) if rng else {})
        return selected_set | range_set

    def as_directories(root_path: Path, indices: Indexes) -> Directories:
        return frozenset(root_path / f"{subdir:0>2}" for subdir in indices)

    indices = merge(selected, rng)
    if not indices:
        return None
    return as_directories(root_path, indices)


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


def setup(vitae: Vitae) -> None:
    """Set environment."""
    logs = Path("logs")

    if vitae.in_development:
        # Since this will run multiple times, this is better to erase logs
        # to avoid unnecessary confusion with older logs.
        erase_logs(logs)

    create_logs(logs)
    redirect_loguru_to(logs / "vitae.log")
    setup_database(vitae)
