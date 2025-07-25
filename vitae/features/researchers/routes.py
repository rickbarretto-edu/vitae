from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from vitae.features.researchers.repository.researchers import (
    ResearchersInDatabase,
)
from vitae.features.researchers.usecases.search import SearchResearchers
from vitae.infra.database import Database
from vitae.settings.vitae import Vitae

router = APIRouter()
templates = Jinja2Templates("vitae/features/researchers/templates")


@router.get("/", response_class=HTMLResponse)
def show_search(request: Request, query: str | None = None):
    vitae = Vitae.from_toml(Path("vitae.toml"))
    database = Database(vitae.postgres.engine)

    researchers = ResearchersInDatabase(database)
    search = SearchResearchers(researchers)

    researchers = (
        search.by_id(query)
        if query
        else []
    )

    return templates.TemplateResponse(
        "search.html",
        {
            "request": request,
            "researchers": researchers,
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
