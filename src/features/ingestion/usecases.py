from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable, Protocol, Self

from src.features.ingestion import scanners as strategy
from src.features.ingestion.parsing import CurriculumParser
from src.lib.panic import panic

if TYPE_CHECKING:
    from pathlib import Path

    from src.features.ingestion.repository import Researchers

__all__ = [
    "Ingestion",
]

 

