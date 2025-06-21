import cyclopts

from src.features.ingestion.cli import app as ingestion_app


def cli() -> None:
    app = cyclopts.App(name="vitae")
    app.command(ingestion_app)
    app()


if __name__ == "__main__":
    cli()
