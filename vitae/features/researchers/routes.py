from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from vitae.features.researchers.repository import (
    FiltersInDatabase,
    ResearchersInDatabase,
)
from vitae.features.researchers.schemes.filters import ChoosenFilters
from vitae.features.researchers.usecases import (
    LoadFilters,
    SearchResearchers,
    SortingOrder,
)
from vitae.infra.database import Database
from vitae.settings.vitae import Vitae

router = APIRouter()
templates = Jinja2Templates("vitae/features/researchers/templates")


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
        "search.html",
        {
            "request": request,
            "filters": all_filters,
        },
    )


@router.get("/search", response_class=HTMLResponse)
def show_search(
    request: Request,
    query: str = "",
    sort: str | None = None,
    country: str | None = None,
    state: str | None = None,
    title: str | None = None,
    expertise: str | None = None,
):
    vitae = Vitae.from_toml(Path("vitae.toml"))
    database = Database(vitae.postgres.engine)

    all_filters = load_filters(database)

    search = SearchResearchers(ResearchersInDatabase(database))
    results = search.query(
        query,
        order_by=SortingOrder(sort) if sort else None,
        filter_by=ChoosenFilters(
            country=country,
            state=state,
            started=title,
            expertise=expertise,
        ),
    )

    return templates.TemplateResponse(
        "search.html",
        {
            "request": request,
            "results": results,
            "filters": all_filters,
        },
    )


@router.get("/researcher/{id}/export", response_class=JSONResponse)
def export_researcher(id: str):
    # Usecase go here...
    pass
