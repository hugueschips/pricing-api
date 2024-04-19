import uvicorn
from fastapi import FastAPI

from pricing.api.v0 import firebase
from pricing.api.v0 import quote as v0

app = FastAPI(description="Embrace the power of simplicity!")

app.include_router(firebase.router)
app.include_router(v0.router)


def start() -> None:
    """Launched with `poetry run start` at root level"""
    uvicorn.run("pricing.main:app", host="127.0.0.1", port=8000, reload=True)
