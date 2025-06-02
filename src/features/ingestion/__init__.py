"""Ingestion package.

This package scan all XMLs files, parses it and
bring data to the system.

"""

from . import converter, schema
from .scanner import CurriculaScheduler

__all__ = [
    "CurriculaScheduler",
    "converter",
    "schema",
]
