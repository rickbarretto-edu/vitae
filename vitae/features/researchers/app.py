from fastapi import FastAPI

from .routes import router

def main():
    app = FastAPI()
    app.include_router(router)
    return app