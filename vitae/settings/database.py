"""Database Settings for general purpose.

This module is a higher level version of `infra.database.settings`,
and this should not rely on any external database related package.

For each feature, use this module instead of the original one.
"""

from vitae.infra.database.settings import setup_database

__all__ = ["setup_database"]
