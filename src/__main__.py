from pathlib import Path

from src.database.database_config import database_config
from src.database.database_creation import new_database
from src.pipeline_etl.extract.dir_scanning import scan_directory
from src.utils.load_env import load_env


def curricula() -> Path:
    """Returns the absolute path to the Curricula's directory.

    Notes
    -----
    - To change the Curricula's directory, update the `CURRICULA_DIRECTORY`
        variable in your `.env` file. Both relative and absolute paths are supported.
    - If there is no `CURRICULA_DIRECTORY`, the default value is `all_files`.
    - The function ensures that the resolved path exists and is a directory.

    Returns
    -------
    Path
        The absolute path to the Curricula's directory.

    Raises
    ------
    AssertionError
        If the resolved path does not exist or is not a directory.
    """

    directory = Path(load_env.directory or "all_files").absolute()
    assert directory.exists() or directory.is_dir()

    return directory


if __name__ == "__main__":
    new_database()
    database_config.migrate()
    scan_directory(curricula())
