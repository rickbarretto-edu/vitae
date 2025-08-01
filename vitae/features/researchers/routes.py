from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse

from vitae.features.researchers.repository import (
    FiltersInDatabase,
    ResearchersInDatabase,
)
from vitae.features.researchers.schemes import ChoosenFilters
from vitae.features.researchers.templates import templates
from vitae.features.researchers.usecases import (
    LoadFilters,
    SearchResearchers,
    SortingOrder,
)
from vitae.infra.database import Database
from vitae.settings.vitae import Vitae

router = APIRouter()


def load_filters(database: Database):
    return LoadFilters(FiltersInDatabase(database)).all


@router.get("/", response_class=HTMLResponse)
def home(
    request: Request,
):
    vitae = Vitae.from_toml(Path("vitae.toml"))
    database = Database(vitae.postgres.engine)

    all_filters = load_filters(database)

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
    # Requirements Setup
    vitae = Vitae.from_toml(Path("vitae.toml"))
    database = Database(vitae.postgres.engine)
    all_filters = load_filters(database)

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


@router.get("/researcher/{id}/export", response_class=JSONResponse)
def export_researcher(id: str):
    # Usecase go here...
    pass
