from dataclasses import dataclass
from pathlib import Path
import tomllib

__all__ = ["vitae", "VitaeSettings"]


@dataclass(frozen=True, kw_only=True)
class PostgresUser:
    """Postgres' Database User Settings"""

    name: str = "postgres"
    password: str

    def __post_init__(self):
        assert self.name
        assert self.password

    def __str__(self) -> str:
        return f"{self.name}:{self.password}"


@dataclass(frozen=True, kw_only=True)
class PostgresDatabase:
    """Postgres' Database Settings"""

    name: str
    host: str = "127.0.0.1"
    port: int = 5433

    def __post_init__(self):
        assert self.name
        assert self.host
        assert self.port

    def __str__(self) -> str:
        return f"{self.host}:{self.port}/{self.name}"


@dataclass(frozen=True, kw_only=True)
class PostgresSettings:
    """Postgres' Settings"""

    user: PostgresUser
    db: PostgresDatabase

    @property
    def url(self) -> str:
        """Postgres URL from vitae.toml file"""
        return f"postgresql+psycopg://{self.user}@{self.db}"


@dataclass(frozen=True, kw_only=True)
class PathsSettings:
    """Paths' Settings for Vitae
    
    Note
    ----
    `_curricula` must exist and be a directory.
    """
    _curricula: Path = Path("all_files")
    alembic: Path = Path("alembic.ini")

    def __post_init__(self):
        assert self._curricula.exists() or self._curricula.is_dir()
        assert self.alembic.is_file()

    @property
    def curricula(self) -> Path:
        """Absolute curricula's directory.

        Note
        ----
        This property exists to ensure curricula's path is always absolute.
        """
        return self._curricula.absolute()


@dataclass
class VitaeSettings:
    """Settings loaded from vitae.toml"""

    postgres: PostgresSettings
    paths: PathsSettings

    @classmethod
    def load(cls) -> "VitaeSettings":
        """Load configuration from vitae.toml file"""
        config_path = Path(__file__).parent.parent.parent / "vitae.toml"

        with open(config_path, "rb") as f:
            data = tomllib.load(f)

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
                ),
            )

            paths: dict = data.get("paths") or {}
            paths_settings = PathsSettings(
                _curricula=Path(paths.get("curricula") or "all_files"),
                alembic=Path(paths.get("alembic", "alembic.ini")),
            )

            return cls(postgres=postgres_settings, paths=paths_settings)


vitae = VitaeSettings.load()
