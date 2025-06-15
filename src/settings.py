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

    @property
    def in_development(self) -> bool:  # noqa: D102
        return not self.in_production


def load() -> VitaeSettings:
    """Load configuration from `vitae.toml` file.

    Returns
    -------
    VitaeSettings
        The loaded settings from the vitae.toml file.

    """
    config_path = Path(__file__).parent.parent / "vitae.toml"

    with config_path.open("rb") as f:
        data: dict[str, Any] = tomllib.load(f)

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
