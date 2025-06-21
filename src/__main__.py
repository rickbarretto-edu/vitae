import cyclopts

from src.features.ingestion.cli import app as ingestion_app


def cli() -> cyclopts.App:
    app = cyclopts.App(name="vitae")
    app.command(ingestion_app)

    return app


if __name__ == "__main__":
    app = cli()
    app()
