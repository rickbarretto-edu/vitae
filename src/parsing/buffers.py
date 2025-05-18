from dataclasses import dataclass
from typing import Callable

from src.lib.buffer import Buffer


@dataclass(kw_only=True)
class CurriculaBuffer:
    general: Buffer
    professions: Buffer
    research_areas: Buffer
    educations: Buffer
