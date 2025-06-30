"""Lower level settings for database that deals with details.

This module should not be imported from your features,
instead, use `vitae.settings` one.

This one deals with external database dependencies.
"""

from sqlmodel import SQLModel

from vitae.settings.vitae import Vitae


def setup_database(vitae: Vitae) -> None:
    """Setups database."""
    # ``models`` module must be evaluated before create or drop it.
    # That is why this imports an unused variable inside this function.
    from vitae.infra.database import tables  # noqa: F401, PLC0415

    if vitae.in_development:
        # Since the dataset for development is far smaller than the production
        # and we run it multiple times to check everything before the ingestion,
        # was decided to rewrite the whole database instead.
        SQLModel.metadata.drop_all(vitae.postgres.engine)
        SQLModel.metadata.create_all(vitae.postgres.engine)

