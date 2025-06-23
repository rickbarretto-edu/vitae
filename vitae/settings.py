"""Environment Settings."""

from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
import tomllib

__all__ = ["VitaeSettings"]


@dataclass(frozen=True, kw_only=True)
class PostgresUser:
    """Postgres' Database User Settings."""

    name: str = "postgres"
    password: str

    def __post_init__(self) -> None:
        if not all((self.name, self.password)):
            message: str = f"Missing fields {self}"
            raise ValueError(message)

    def __str__(self) -> str:
        return f"{self.name}:{self.password}"


@dataclass(frozen=True, kw_only=True)
class PostgresDatabase:
    """Postgres' Database Settings."""

    name: str
    host: str = "127.0.0.1"
    port: int = 5433

    flush_every: int = 100

    def __post_init__(self) -> None:
        if not all((self.name, self.host, self.port)):
            message: str = f"Missing fields {self}"
            raise ValueError(message)

    def __str__(self) -> str:
        return f"{self.host}:{self.port}/{self.name}"


@dataclass(frozen=True, kw_only=True)
class PostgresSettings:
    """Postgres' Settings."""

    user: PostgresUser
    db: PostgresDatabase

    @property
    def url(self) -> str:
        """Postgres URL from vitae.toml file."""
        return f"postgresql+psycopg://{self.user}@{self.db}"

    @cached_property
    def engine(self) -> Engine:
        """SQLAlchemy Engine."""
        return create_engine(self.url)

    @cached_property
    def verbose_engine(self) -> Engine:
        """SQLAlchemy Engine.

        The engine is verbose, so every event will be logged on terminal.
        """
        return create_engine(self.url, echo=True)


@dataclass(frozen=True, kw_only=True)
class PathsSettings:
    """Paths' Settings for Vitae.

    Note:
    ----
    `_curricula` must exist and be a directory.

    """

    _curricula: Path = Path("all_files")

    def __post_init__(self) -> None:
        if not self._curricula.exists():
            message: str = "Curricula must exist"
            raise ValueError(message)

        if not self._curricula.is_dir():
            message: str = "Curricula must be a directory"
            raise ValueError(message)

    @property
    def curricula(self) -> Path:
        """Absolute curricula's directory.

        Note:
        ----
        This property exists to ensure curricula's path is always absolute.

        """
        return self._curricula.absolute()


@dataclass(frozen=True, kw_only=True)
class VitaeSettings:
    """Settings loaded from `vitae.toml`."""

    postgres: PostgresSettings
    paths: PathsSettings
    in_production: bool = False

    @staticmethod
    def from_toml(file: Path) -> "VitaeSettings":
        return _from_file(file)

    @property
    def in_development(self) -> bool:  # noqa: D102
        return not self.in_production


def _from_file(config_file: Path) -> VitaeSettings:
    """Load configuration from `config_file` TOML file."""  # noqa: DOC201
    with config_file.open("rb") as f:
        return _from_dict(tomllib.load(f))


def _from_toml(content: str) -> VitaeSettings:
    """Load configuration from TOML string."""  # noqa: DOC201
    return _from_dict(tomllib.loads(content))


def _from_dict(data: dict[str, Any]) -> VitaeSettings:
    """Parse data from dictionary.

    Use the functions `_from_file` or `_from_toml` to get `data`.
    """  # noqa: DOC201
    in_production: bool = data.get("in_production", False)
    postgres: dict = data.get("postgres") or {}
    postgres_settings = PostgresSettings(
        user=PostgresUser(
            name=postgres["user"]["name"],
            password=postgres["user"]["password"],
        ),
        db=PostgresDatabase(
            name=postgres["database"]["name"],
            host=postgres["database"].get("host", "127.0.0.1"),
            port=postgres["database"].get("port", 5433),
            flush_every=postgres["database"].get("flush_every", 100),
        ),
    )

    paths: dict = data.get("paths") or {}
    paths_settings = PathsSettings(
        _curricula=Path(paths.get("curricula") or "all_files"),
    )

    return VitaeSettings(
        in_production=in_production,
        postgres=postgres_settings,
        paths=paths_settings,
    )
