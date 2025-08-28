import time
from fastapi import FastAPI, Request
from loguru import logger

from .routes import router


def main():
    app = FastAPI()
    app.include_router(router)

    @app.middleware("http")
    async def log_request_runtime(request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = (time.perf_counter() - start_time) * 1000  # ms
        
        logger.info(
            "{method} {path} - {status_code} - {time:.2f} ms",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            time=process_time,
        )
        return response


    return app