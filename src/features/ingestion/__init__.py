"""Ingestion package.

This package scan all XMLs files, parses it and
bring data to the system.

"""

from pathlib import Path
from typing import Callable

from src.features.database import Database
from src.features.ingestion.scanner import (
    parallel_scanning,
    process_directory,
    serial_scanning,
)

from . import converter, schema

__all__ = [
    "converter",
    "ingestion",
    "parallel_scanning",
    "schema",
    "serial_scanning",
]


def ingestion(database: Database) -> Callable[[Path], None]:
    """Process a directory containing XML files."""  # noqa: DOC201
    return lambda subdir: process_directory(database, subdir)
