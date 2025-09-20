from __future__ import annotations

import functools
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse

from vitae.features.researchers.model.researcher import Researcher
from vitae.features.researchers.repository import (
    FiltersInDatabase,
    ResearchersInDatabase,
)
from vitae.features.researchers.schemes import ChoosenFilters
from vitae.features.researchers.schemes.filters import Filters
from vitae.features.researchers.templates import load_templates
from vitae.features.researchers.usecases import (
    LoadFilters,
    SearchResearchers,
    SortingOrder,
)
from vitae.infra.database import Database
from vitae.settings.vitae import Vitae


# =~=~=~=~=~=~= Server Configuration =~=~=~=~=~=~=

vitae = Vitae.from_toml(Path("vitae.toml"))
database = Database(vitae.postgres.engine)

router = APIRouter()
templates = load_templates(vitae)

all_filters = LoadFilters(FiltersInDatabase(database)).all


# =~=~=~=~=~=~= EndPoints =~=~=~=~=~=~=


@router.get("/", response_class=HTMLResponse)
def home(
    request: Request,
):

    return templates.TemplateResponse(
        "SearchPage.jinja",
        {
            "request": request,
            "filters": all_filters,
            "page": 0,
        },
    )


@router.get("/search", response_class=HTMLResponse)
def show_search(
    request: Request,
    query: str = "",
    page: int = 1,
    sort: str | None = None,
    country: str | None = None,
    state: str | None = None,
    started: str | None = None,
    has_finished: bool = False,
    expertise: str | None = None,
):

    # Feature Setup
    search = SearchResearchers(ResearchersInDatabase(database))
    choosen_filters = ChoosenFilters(
        country=country,
        state=state,
        started=started,
        has_finished=has_finished,
        expertise=expertise,
    )

    results = search.query(
        query,
        order_by=SortingOrder(sort) if sort else None,
        filter_by=choosen_filters,
        page=page,
    )

    return templates.TemplateResponse(
        "SearchPage.jinja",
        {
            "request": request,
            "results": results,
            "filters": all_filters,
            "page": page,
        },
    )


@router.get("/export")
def export_all(
    request: Request,
    query: str = "",
    country: str | None = None,
    state: str | None = None,
    started: str | None = None,
    has_finished: bool = False,
    expertise: str | None = None,
) -> JSONResponse:
    search = SearchResearchers(ResearchersInDatabase(database))
    choosen_filters = ChoosenFilters(
        country=country,
        state=state,
        started=started,
        has_finished=has_finished,
        expertise=expertise,
    )

    found: list[Researcher] = search.query(
        query,
        order_by=None,
        filter_by=choosen_filters,
        page=None,
    )

    result = {
        researcher.links.lattes.id: str(researcher.this.name)
        for researcher in found
    }

    print(result)
    return JSONResponse(content=result)