"""Ingestion package.

This package scan all XMLs files, parses it and
bring data to the system.

Usage
-----
    # For serial scanning ingestion
    serial_scanning(Path("all_files"), ingestion(database))

    # For parallel scanning ingestion
    arallel_scanning(Path("all_files"), ingestion(database))

"""

from src.features.ingestion import debug
from src.features.ingestion.repository import Researchers
from src.features.ingestion.scanner import parallel_scanning, serial_scanning
from src.features.ingestion.usecases import Ingestion
from src.lib.panic import panic

from . import schema

__all__ = [
    "Ingestion",
    "Researchers",
    "debug",
    "panic",
    "parallel_scanning",
    "schema",
    "serial_scanning",
]
