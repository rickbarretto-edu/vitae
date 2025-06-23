import cyclopts

from vitae.features.ingestion.cli import app as ingestion_app
from vitae.features.ingestion.cli import ingest


def cli() -> None:
    app = cyclopts.App(name="vitae")
    app.command(ingestion_app)
    app()


def debug_ingest() -> None:
    ingest(buffer=5)


if __name__ == "__main__":
    cli()
