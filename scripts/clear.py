from pathlib import Path
import shutil

project = Path()


def _clear(path: Path):
    if path.exists():
        print(f"Clearing {path}...")
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
    else:
        print(f"{path} does not exist.")


def cache():
    pytest = project / ".pytest_cache"
    ruff = project / ".ruff_cache"
    pycache = list(project.glob("**/__pycache__"))

    _clear(pytest)
    _clear(ruff)
    for cache in pycache:
        _clear(cache)


def log():
    logs = project / "logs"

    _clear(logs)