import cyclopts

from vitae.features.bootstrap.cli import app as bootstrap_app
from vitae.features.ingestion.cli import app as ingestion_app
from vitae.features.researchers.cli import app as researchers_app

def cli() -> None:
    """Integrates all features into one CLI."""
    app = cyclopts.App(name="vitae")
    app.command(ingestion_app)
    app.command(bootstrap_app)
    app.command(researchers_app)
    app()


if __name__ == "__main__":
    cli()
