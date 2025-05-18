from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import eliot

from src.parsing.buffers import CurriculaBuffer
from src.parsing.load import load
from src.parsing.parser import parser
from src.utils.panic import panic
from src.utils.buffer import Buffer

__all__ = ["scan_directory"]


@eliot.log_call(action_type="scanning")
def scan_directory(curricula_folder: Path):
    """
    Scan the directory containing Lattes curricula and process all subdirectories.

    This function identifies the current working directory, verifies the existence
    of a "repo" directory containing subdirectories of curricula, and processes
    each subdirectory concurrently using a thread pool. Each subdirectory is expected
    to contain zipped curricula files, which are parsed and processed.

    Raises
    ------
    Exception
        If an error occurs during the scanning or processing of directories.

    Notes
    -----
    - The function logs the progress and any errors encountered during execution.
    - Subdirectories are processed in parallel to improve performance.
    """
    if not curricula_folder.exists():
        panic(f"Curricula directory does not exist: {curricula_folder}")

    if not curricula_folder.is_dir():
        panic(f"Curricula's path must be a directory: {curricula_folder}")

    with ThreadPoolExecutor(max_workers=8) as executor:
        for folder in curricula_folder.iterdir():
            executor.submit(process_subdir, folder)


@eliot.log_call(action_type="scanning")
def process_subdir(subdirectory: Path):
    """Process all curriculum files in a subdirectory.

    Scans the given subdirectory, processes each curriculum file using the parser,
    manages data buffers, and periodically flushes them to the database.
    """

    if not subdirectory.exists():
        panic(f"Subdirectory does not exist: {subdirectory}")

    for curriculum in subdirectory.glob("*.xml"):
        process_curriculum(curriculum)


@eliot.log_call(action_type="scanning")
def process_curriculum(curriculum: Path):
    def buffer(action) -> Buffer:
        return Buffer(max=2).on_flush(action)

    curricula_buffer = CurriculaBuffer(
        general=buffer(load.upsert_researcher),
        professions=buffer(load.upsert_professional_experience),
        research_areas=buffer(load.upsert_academic_background),
        educations=buffer(load.upsert_research_area),
    )

    parser.open_curriculum(curriculum, curricula_buffer)
