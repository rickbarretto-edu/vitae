from pathlib import Path
from typing import Annotated, Literal

import cyclopts
from cyclopts import Parameter
from cyclopts.types import PositiveInt

from vitae.shared import database, vitae

from . import scanners
from .repository import Researchers
from .usecase import Ingestion

__all__ = ["app", "ingest"]

app = cyclopts.App(name="ingest")

type Indexes = frozenset[int]
type SelectedIndexes = list[int] | None
type IndexRange = tuple[int, int] | None
type Directories = frozenset[Path]


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


@app.default
def ingest(
    indexes: Annotated[
        list[int] | None,  # noqa: FA102
        Parameter(name=["--indexes", "-i"]),
    ] = None,
    _range: Annotated[IndexRange, Parameter(name=["--range", "-r"])] = None,
    strategy: Annotated[
        Literal["serial", "pool"],
        Parameter(name=["--strategy", "-s"]),
    ] = "pool",
    buffer: Annotated[int, Parameter(name=["--buffer", "-b"])] = 50,
    workers: Annotated[PositiveInt, Parameter(name=["--workers", "-w"])] = 8,
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

    strategy : Literal["serial", "pool"], default="pool"
        Method used to scan the directory containing XML files.
        Use "serial" for sequential scanning or "pool" for parallel scanning.

    buffer : int, default=50
        Number of researchers to buffer before committing to the database.
        Use higher numbers on production.

    workers: PositiveInt
        Machine available cores. When using `pool` strategy.

    """
    root_directory = vitae.paths.curricula
    scan_only = merge_indexes(root_directory, indexes, _range)
    repository = Researchers(db=database, every=buffer)
    scanner = {
        "serial": scanners.Serial(scan_only=scan_only),
        "pool": scanners.Pool(scan_only=scan_only, max_workers=workers),
    }[strategy]
    processed_curricula = curricula_xml_from(
        Path("logs/ingestion/processed.log"),
    )

    ingestion = Ingestion(
        researchers=repository,
        scanner=scanner,
        files=root_directory,
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
