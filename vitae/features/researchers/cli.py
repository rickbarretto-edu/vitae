import sys
import subprocess

import cyclopts
import uvicorn
from fastapi import FastAPI

from vitae.features.researchers.routes import router

app = cyclopts.App(name=["web", "ui", "researchers", "search"])


@app.default
def web(production: bool = False) -> None:
    """Runs Web UI for searching Researchers.
    
    You can search, filter and also export as Lucy Lattes CSV files.
    """

    args = [
        sys.executable,
        "-m",
        "uvicorn",
        "vitae.features.researchers.routes:fastapi_app",
        "--host",
        "0.0.0.0" if production else "127.0.0.1",
        "--port",
        "8000",
    ]

    if production:
        args += ["--workers", "4"]
    else:
        args += ["--reload"]
    subprocess.run(args)
