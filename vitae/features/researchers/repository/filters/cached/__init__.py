"""In Memory data fetched from database.

Latest Update: 
    27/08/2025

This module contains fetched data from the SQL Database,
to reduce overhead when loading the application for the first time, 
I think this is a good idea.
"""

from functools import cached_property
from pathlib import Path
from typing import Sequence
import attrs


@attrs.frozen
class FiltersInCache:

    def _from_file(self, file: str) -> list[str]:
        base = Path("vitae/features/researchers/repository/filters/cached")
        with (base / file).open("r", encoding="utf-8", errors="replace") as f:
            return f.readlines()

    @cached_property
    def countries(self) -> Sequence[str]:
        return self._from_file("countries.txt")
    
    @cached_property
    def states(self) -> Sequence[str]:
        return self._from_file("states.txt")

    @cached_property
    def titles(self) -> Sequence[str]:
        return self._from_file("degrees.txt")

    @cached_property
    def expertises(self) -> Sequence[str]:
        return []