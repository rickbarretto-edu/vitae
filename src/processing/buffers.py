from dataclasses import dataclass

from src.lib.buffer import Buffer


@dataclass(kw_only=True)
class CurriculaBuffer:
    general: Buffer
    professions: Buffer
    research_areas: Buffer
    educations: Buffer
