from fastapi import FastAPI

from api_gateway.routers import gateway


_app = None


def get_app():
    global _app
    if not _app:
        _app = FastAPI(title="Zunlix", version="0.1.1", description="Zunlix")
        _app.include_router(gateway)

    return _app
