import asyncio
import sys
from fastapi.responses import RedirectResponse
import uvicorn

from .bootstrap import create_app

app = create_app()


@app.get("/")
def index():
    return RedirectResponse(url="/docs")


@app.get("/front")
def to_ui():
    return RedirectResponse(url="https://app.my-narae.link/")


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
