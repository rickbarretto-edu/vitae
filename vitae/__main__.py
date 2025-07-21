import cyclopts
from fastapi import FastAPI

from vitae.features.bootstrap.cli import app as bootstrap_app
from vitae.features.ingestion.cli import app as ingestion_app
from vitae.features.ingestion.cli import ingest
from vitae.features.researchers.routes import router as web_router


def web() -> None:
    app = FastAPI()
    app.include_router(web_router)


def cli() -> None:
    app = cyclopts.App(name="vitae")
    app.command(ingestion_app)
    app.command(bootstrap_app)
    app()


def debug_ingest() -> None:
    ingest(buffer=5)


if __name__ == "__main__":
    cli()
