"""Setup the application settings.

The purpose of this module is to handle and abstract all the initialization
of the Application system, such as logging and database.

This module deals with external dependencies,
so the main module should be independent from them.
"""

from pathlib import Path

from vitae.settings.database import setup_database
from vitae.settings.logging import create_logs, erase_logs, redirect_loguru_to
from vitae.settings.vitae import Vitae

__all__ = [
    "new_vitae",
]

# =~=~=~ Public ~=~=~=


def new_vitae() -> Vitae:
    """Create a new vitae application.

    This function loads Vitae's settings and sets up the whole application,
    such as databases and logging systems.

    Returns
    -------
    New Vitae's Settings from ``vitae.toml``

    """
    vitae = Vitae.from_toml(Path("vitae.toml"))
    setup_vitae(vitae)
    return vitae


def setup_vitae(vitae: Vitae) -> None:
    """Setups Vitae's Logging and database."""
    logs = Path("logs")

    if vitae.in_development:
        # Since this will run multiple times, this is better to erase logs
        # to avoid unnecessary confusion with older logs.
        erase_logs(logs)

    create_logs(logs)
    redirect_loguru_to(logs / "vitae.log")

    setup_database(vitae)
