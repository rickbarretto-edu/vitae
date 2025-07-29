from __future__ import annotations

from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from vitae.features.researchers.repository import (
    FiltersInDatabase,
    ResearchersInDatabase,
)
from vitae.features.researchers.usecases.filters import LoadFilters
from vitae.features.researchers.usecases.search import (
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
    all_filters: Annotated[LoadFilters, Depends(load_filters)],
):
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
    all_filters: Annotated[LoadFilters, Depends(load_filters)],
    query: str,
    sort: str | None = None,
):
    vitae = Vitae.from_toml(Path("vitae.toml"))
    database = Database(vitae.postgres.engine)

    search = SearchResearchers(ResearchersInDatabase(database))
    results = search.query(
        query,
        SortingOrder(sort) if sort else None,
    )

    return templates.TemplateResponse(
        "search.html",
        {
            "request": request,
            "results": results,
            "filters": all_filters,
        },
    )


@router.get("/researcher/{id}", response_class=HTMLResponse)
def show_researcher_detail(request: Request, id: str):
    # Usecase go here...
    researcher = None  # Placeholder
    return templates.TemplateResponse(
        "detail.html",
        {"request": request, "researcher": researcher},
    )


@router.get("/researcher/{id}/export", response_class=JSONResponse)
def export_researcher(id: str):
    # Usecase go here...
    pass
