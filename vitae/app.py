from pathlib import Path
import sys

from flaskwebgui import FlaskUI

from vitae.features.researchers.app import main


def create_config_file():
    example = """
[project]
in_production = false

[postgres.user]
name = "postgres_user"
password = "your_secure_password"

[postgres.database]
host = "localhost"
port = 5432
name = "your_database_name"
flush_every = 100

[paths]
curricula = "path/to/your/curricula/files"
    """
    config_file = Path("vitae.toml")
    if not config_file.exists():
        with config_file.open("+w", encoding="utf-8") as file:
            file.write(example)


def redirect_console_to_logfile(logfile: Path):
    log_file = logfile.open("+a", encoding="utf-8")
    sys.stdout = log_file
    sys.stderr = log_file

def start_app():
    FlaskUI(app=main(), server="fastapi").run()


if __name__ == "__main__":
    redirect_console_to_logfile(Path("vitae.log"))
    create_config_file()
    start_app()
