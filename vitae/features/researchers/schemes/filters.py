from __future__ import annotations

from typing import TypedDict


class Filters(TypedDict):
    countries: list[str]
    states: list[str]
    titles: list[str]
    expertises: list[str]


class ChoosenFilters(TypedDict, total=True):
    country: str | None
    state: str | None
    started: str | None
    has_finished: bool | None
    expertise: str | None
