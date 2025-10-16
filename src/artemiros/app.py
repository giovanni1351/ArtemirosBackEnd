from typing import Any, Literal

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from routes import levels, token
from uvicorn import run

app = FastAPI()
app.include_router(token.router)
app.include_router(levels.router)


def custom_openapi() -> dict[str, Any]:
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema: dict[str, Any] = get_openapi(
        title="Artemiro BACKEND",
        version="0.0.1",
        summary="Sistema de monitoramento dos jogadores",
        description="O acesso desta api é para jogadores",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/heath")
async def health() -> dict[str, Literal["Ok"]]:
    return {"status": "Ok"}


if __name__ == "__main__":
    run("app:app", reload=True)
