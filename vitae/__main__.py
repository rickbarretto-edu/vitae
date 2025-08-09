import cyclopts
from fastapi import FastAPI
import uvicorn

from vitae.features.bootstrap.cli import app as bootstrap_app
from vitae.features.ingestion.cli import app as ingestion_app

def cli() -> None:
    app = cyclopts.App(name="vitae")
    app.command(ingestion_app)
    app.command(bootstrap_app)
    app()


if __name__ == "__main__":
    cli()
