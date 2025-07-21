from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates("vitae/features/researcher/templates")


@router.get("/", response_class=HTMLResponse)
def show_search(request: Request, query: str):
    # Usecase go here...
    return templates.TemplateResponse("search.html", {"request": request})


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
