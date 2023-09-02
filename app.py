import uvicorn

from api_gateway.application import get_app

app = get_app()

if __name__ == "__main__":
    uvicorn.run(app="app:app")