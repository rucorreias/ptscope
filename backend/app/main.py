from fastapi import FastAPI

from app.api.router import api_router

app = FastAPI(
    title="PTScope API",
    description="Public territorial intelligence API for Portugal",
    version="0.1.0",
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["root"])
def read_root() -> dict[str, str]:
    """Return a minimal status payload for the public API root."""
    return {"project": "PTScope", "status": "running"}
