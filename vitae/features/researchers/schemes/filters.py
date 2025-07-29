from typing import TypedDict


class Filters(TypedDict):
    countries: list[str]
    states: list[str]
    titles: list[str]
    expertises: list[str]
