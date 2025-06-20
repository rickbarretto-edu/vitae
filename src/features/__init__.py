from dataclasses import dataclass

from src.features.ingestion.usecases import Ingestion

__all__ = [
    "Features",
]


@dataclass
class Features:
    ingestion: Ingestion
