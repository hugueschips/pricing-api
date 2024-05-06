import uvicorn
from fastapi import FastAPI

from pricing.api.v0 import basic_auth, firebase, quote

app = FastAPI(description="Embrace the power of simplicity!")

app.include_router(basic_auth.router)
app.include_router(firebase.router)
app.include_router(quote.router)


def start() -> None:
    """Launched with `poetry run start` at root level"""
    uvicorn.run("pricing.main:app", host="127.0.0.1", port=8000, reload=True)
