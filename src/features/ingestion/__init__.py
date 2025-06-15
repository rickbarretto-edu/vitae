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

from src.features.ingestion import debug, scanners
from src.features.ingestion.repository import Researchers
from src.features.ingestion.usecases import Ingestion

__all__ = [
    "Ingestion",
    "Researchers",
    "debug",
    "scanners",
]
