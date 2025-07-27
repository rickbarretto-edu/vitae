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
def home(request: Request):
    return templates.TemplateResponse(
        "search.html",
        {
            "request": request,
        },
    )


@router.get("/search", response_class=HTMLResponse)
def show_search(request: Request, query: str):
    vitae = Vitae.from_toml(Path("vitae.toml"))
    database = Database(vitae.postgres.engine)

    search = SearchResearchers(ResearchersInDatabase(database))
    results = search.query(query)

    return templates.TemplateResponse(
        "search.html",
        {
            "request": request,
            "results": results,
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
