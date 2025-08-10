import sys
import subprocess

import cyclopts
from fastapi import FastAPI
import uvicorn

from vitae.features.researchers.routes import router

app = cyclopts.App(name=["web", "ui", "researchers", "search"])


@app.default
def web(production: bool = False) -> None:
    """Runs Web UI for searching Researchers.
    
    You can search, filter and also export as Lucy Lattes CSV files.
    """

    uvicorn.run(
        "vitae.features.researchers.app:main",
        host="0.0.0.0" if production else "127.0.0.1",
        port=8000,
        reload=not production,
        log_level="info" if production else "debug",
        workers=4 if production else 1,
    )
