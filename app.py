#!/usr/bin/env python3
import contextlib as __scriptmerge_contextlib


@__scriptmerge_contextlib.contextmanager
def __scriptmerge_temporary_dir():
    import tempfile
    import shutil

    dir_path = tempfile.mkdtemp()
    try:
        yield dir_path
    finally:
        shutil.rmtree(dir_path)


with __scriptmerge_temporary_dir() as __scriptmerge_working_dir:

    def __scriptmerge_write_module(path, contents):
        import os, os.path

        def make_package(path):
            parts = path.split("/")
            partial_path = __scriptmerge_working_dir
            for part in parts:
                partial_path = os.path.join(partial_path, part)
                if not os.path.exists(partial_path):
                    os.mkdir(partial_path)
                    with open(os.path.join(partial_path, "__init__.py"), "wb") as f:
                        f.write(b"\n")

        make_package(os.path.dirname(path))

        full_path = os.path.join(__scriptmerge_working_dir, path)
        with open(full_path, "wb") as module_file:
            module_file.write(contents)

    import sys as __scriptmerge_sys

    __scriptmerge_sys.path.insert(0, __scriptmerge_working_dir)
    __scriptmerge_write_module('routes/__init__.py', b'')
    __scriptmerge_write_module('routes/atividade.py', b'from database import AsyncSessionDep\r\nfrom fastapi import APIRouter\r\nfrom schemas.atividade import Atividade, AtividadeCreate\r\nfrom utils.aio_helpers import create_item\r\n\r\nrouter = APIRouter(prefix="/atividade", tags=["atividade"])\r\n\r\n\r\n@router.post("/")\r\nasync def create_atividade(\r\n    atividade: AtividadeCreate, session: AsyncSessionDep\r\n) -> Atividade:\r\n    return await create_item(session, Atividade, atividade.model_dump())\r\n')
    __scriptmerge_write_module('database.py', b'from typing import Annotated\r\nfrom urllib.parse import quote_plus\r\n\r\nfrom fastapi import Depends\r\nfrom sqlalchemy import NullPool\r\nfrom settings import LOGGER, SETTINGS\r\nfrom sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine\r\nfrom sqlmodel.ext.asyncio.session import AsyncSession\r\n\r\n\r\ndef generate_connection_string() -> str:\r\n    if SETTINGS.SQLITE_DEV == 1:\r\n        return "sqlite+aiosqlite:///database.db"\r\n    return (\r\n        f"postgresql+asyncpg://{SETTINGS.DB_USER}:{quote_plus(SETTINGS.DB_PASSWORD)}@{SETTINGS.DB_HOST}:"\r\n        f"{SETTINGS.DB_PORT}/{SETTINGS.DB_DATABASE}"\r\n    )\r\n\r\n\r\nasync_engine: AsyncEngine = create_async_engine(\r\n    generate_connection_string(), pool_recycle=30,\r\n    poolclass=NullPool,  # Para ambientes serverless\r\n    connect_args={\r\n        # Desabilita JIT do PostgreSQL para melhor performance em serverless\r\n        "server_settings": {"jit": "off"},\r\n        "command_timeout": 60,\r\n        "timeout": 30,\r\n    } if SETTINGS.SQLITE_DEV == 0 else {}\r\n)\r\n\r\n\r\nasync def get_async_session():  # noqa: ANN201\r\n    LOGGER.debug(\r\n        f"Getting async session to  {SETTINGS.DB_DATABASE=} {generate_connection_string()}"\r\n    )\r\n    async with AsyncSession(async_engine, expire_on_commit=False) as session:\r\n        yield session\r\n\r\n\r\nAsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]\r\n')
    __scriptmerge_write_module('settings.py', b'import logging\r\n\r\nfrom dotenv import load_dotenv\r\nfrom pydantic_settings import BaseSettings\r\n\r\nload_dotenv()\r\n\r\n\r\nclass Settings(BaseSettings):\r\n    DB_USER: str\r\n    DB_PASSWORD: str\r\n    DB_HOST: str\r\n    DB_PORT: str\r\n    DB_DATABASE: str\r\n    LOG_LEVEL: str\r\n    SECRET_KEY: str\r\n    ALGORITHM: str\r\n    ACCESS_TOKEN_EXPIRE_MINUTES: int\r\n    SQLITE_DEV: int\r\n\r\n\r\nSETTINGS = Settings()  # pyright: ignore[reportCallIssue]\r\n\r\nLOGGER = logging.getLogger()\r\n')
    __scriptmerge_write_module('schemas/__init__.py', b'from schemas.atividade import Atividade\r\nfrom schemas.levels import Level\r\nfrom schemas.token import TokenData\r\n\r\n__all__ = [\r\n    "Atividade",\r\n    "Level",\r\n    "TokenData",\r\n]\r\n')
    __scriptmerge_write_module('schemas/atividade.py', b'from datetime import datetime\r\nfrom uuid import UUID\r\n\r\nfrom sqlmodel import (  # pyright: ignore[reportUnknownVariableType]\r\n    Field,  # pyright: ignore[reportUnknownVariableType]\r\n    Relationship,\r\n    SQLModel,\r\n)\r\n\r\nfrom schemas.levels import Level\r\nfrom schemas.token import TokenData\r\n\r\n\r\nclass AtividadeCreate(SQLModel):\r\n    id_level: int = Field(foreign_key="level.id")\r\n    id_token: UUID = Field(foreign_key="tokendata.id")\r\n    atividade: str\r\n\r\n\r\nclass Atividade(AtividadeCreate, table=True):\r\n    id: int = Field(primary_key=True)\r\n    level: Level = Relationship(back_populates="atividades")\r\n    token: TokenData = Relationship(back_populates="atividades")\r\n    created_at: datetime\r\n')
    __scriptmerge_write_module('schemas/levels.py', b'from datetime import datetime\r\nfrom typing import TYPE_CHECKING\r\n\r\nfrom sqlmodel import (  # pyright: ignore[reportUnknownVariableType]\r\n    Field,  # pyright: ignore[reportUnknownVariableType]\r\n    Relationship,\r\n    SQLModel,\r\n)\r\n\r\nif TYPE_CHECKING:\r\n    from schemas.atividade import (\r\n        Atividade,\r\n    )\r\n\r\n\r\nclass LevelCreate(SQLModel):\r\n    nome_level: str\r\n\r\n\r\nclass LevelUpdate(SQLModel):\r\n    id: int\r\n    nome_level: str\r\n\r\n\r\nclass Level(LevelCreate, table=True):\r\n    id: int = Field(primary_key=True)\r\n    created_at: datetime = Field(default_factory=datetime.now)\r\n    atividades: list["Atividade"] = Relationship(back_populates="level")\r\n')
    __scriptmerge_write_module('schemas/token.py', b'from datetime import datetime\r\nfrom typing import TYPE_CHECKING\r\nfrom uuid import UUID, uuid4\r\n\r\nfrom sqlmodel import (\r\n    Field,  # pyright: ignore[reportUnknownVariableType]\r\n    Relationship,\r\n    SQLModel,\r\n)\r\n\r\nif TYPE_CHECKING:\r\n    from schemas.atividade import Atividade\r\n\r\n\r\nclass TokenCreate(SQLModel):\r\n    username: str | None = None\r\n\r\n\r\nclass TokenUpdate(SQLModel):\r\n    id: UUID\r\n    momento_fechamento: datetime | None\r\n\r\n\r\nclass TokenData(SQLModel, table=True):\r\n    id: UUID = Field(primary_key=True, default_factory=uuid4)\r\n    momento_abertura: datetime = Field(default_factory=datetime.now)\r\n    momento_fechamento: datetime | None = Field(default=None)\r\n    atividades: list["Atividade"] = Relationship(back_populates="token")\r\n')
    __scriptmerge_write_module('utils/__init__.py', b'')
    __scriptmerge_write_module('utils/aio_helpers.py', b'from collections.abc import Sequence\r\nfrom datetime import datetime\r\nfrom typing import Any\r\n\r\nfrom database import AsyncSession, AsyncSessionDep\r\nfrom fastapi import HTTPException, status\r\nfrom settings import LOGGER\r\nfrom sqlmodel import SQLModel, select\r\n\r\nfrom utils.logger_decorator import async_log_and_check_error\r\n\r\n# Decorator para logar o retorno da fun\xc3\xa7\xc3\xa3o e verificar se ocorreu algum erro\r\n\r\n\r\n@async_log_and_check_error\r\nasync def create_item[T: SQLModel](\r\n    session: AsyncSession, model: type[T], data: dict[str, Any]\r\n) -> T:\r\n    """Helper gen\xc3\xa9rico para criar"""\r\n    if hasattr(model, "created_at"):\r\n        data["created_at"] = datetime.now()\r\n    if hasattr(model, "updated_at"):\r\n        data["updated_at"] = datetime.now()\r\n\r\n    item: T = model(**data)\r\n    session.add(item)\r\n    await session.commit()\r\n    await session.refresh(item)\r\n    return item\r\n\r\n\r\n@async_log_and_check_error\r\nasync def get_item_or_404[T](\r\n    session: AsyncSession, model: type[T], item_id: object\r\n) -> T:\r\n    """Helper gen\xc3\xa9rico para buscar"""\r\n    item = await session.get(model, item_id)\r\n    if not item:\r\n        LOGGER.warning(f"{model.__name__} n\xc3\xa3o encontrado")\r\n        raise HTTPException(\r\n            status_code=status.HTTP_404_NOT_FOUND,\r\n            detail=f"{model.__name__} n\xc3\xa3o encontrado",\r\n        )\r\n    return item\r\n\r\n\r\n@async_log_and_check_error\r\nasync def update_item[T](\r\n    session: AsyncSessionDep, model: type[T], data: dict[str, object]\r\n) -> T:\r\n    item = await get_item_or_404(session, model, data["id"])\r\n    for key, value in data.items():\r\n        setattr(item, key, value)\r\n    session.add(item)\r\n    await session.commit()\r\n    await session.refresh(item)\r\n    return item\r\n\r\n\r\n@async_log_and_check_error\r\nasync def get_all_items[T](\r\n    session: AsyncSession,\r\n    model: type[T],\r\n    **kwargs: object,\r\n) -> Sequence[T]:\r\n    """Helper gen\xc3\xa9rico para buscar todos os itens"""\r\n    try:\r\n        query = select(model)\r\n        for key, value in kwargs.items():\r\n            query = query.where(getattr(model, key) == value)\r\n        result = await session.exec(query)\r\n        return result.all()\r\n    except Exception as e:\r\n        raise e from e\r\n\r\n\r\n@async_log_and_check_error\r\nasync def delete_item[T](\r\n    session: AsyncSession, model: type[T], item_id: object\r\n) -> None:\r\n    """Helper gen\xc3\xa9rico para deletar"""\r\n    item = await session.get(model, item_id)\r\n    if not item:\r\n        raise HTTPException(\r\n            status_code=status.HTTP_404_NOT_FOUND,\r\n            detail=f"{model.__name__} n\xc3\xa3o encontrado",\r\n        )\r\n    await session.delete(item)\r\n    await session.commit()\r\n\r\n\r\n@async_log_and_check_error\r\nasync def soft_delete_item[T](\r\n    session: AsyncSession, model: type[SQLModel], item_id: object\r\n) -> None:\r\n    """Helper gen\xc3\xa9rico para deletar"""\r\n    item = await session.get(model, item_id)\r\n    if not item:\r\n        raise HTTPException(\r\n            status_code=status.HTTP_404_NOT_FOUND,\r\n            detail=f"{model.__name__} n\xc3\xa3o encontrado",\r\n        )\r\n    item.deleted_at = datetime.now()\r\n    session.add(item)\r\n    await session.commit()\r\n\r\n\r\n@async_log_and_check_error\r\nasync def get_all_itens_by_in_clause[T](\r\n    session: AsyncSession, model: type[T], column: str, ids: list[int]\r\n) -> Sequence[T]:\r\n    """Helper gen\xc3\xa9rico para buscar todos os ids"""\r\n    query = select(model)\r\n    query = query.where(getattr(model, column).in_(ids))\r\n    result = await session.exec(query)\r\n    return result.all()\r\n\r\n\r\n@async_log_and_check_error\r\nasync def remove_item_from_link_table[T](\r\n    session: AsyncSession, model: type[T], item_ids: list[int | str]\r\n) -> T | None:\r\n    """Helper gen\xc3\xa9rico para deletar"""\r\n    item = await session.get(model, item_ids)\r\n    if not item:\r\n        raise HTTPException(\r\n            status_code=status.HTTP_404_NOT_FOUND,\r\n            detail=f"{model.__name__} n\xc3\xa3o encontrado",\r\n        )\r\n    await session.delete(item)\r\n    await session.commit()\r\n    return item\r\n')
    __scriptmerge_write_module('utils/logger_decorator.py', b'from collections.abc import Awaitable, Callable\r\nfrom functools import wraps\r\n\r\nfrom fastapi import HTTPException, status\r\nfrom settings import LOGGER\r\n\r\n\r\ndef async_log_and_check_error[**IN, OUT](\r\n    func: Callable[IN, Awaitable[OUT]],\r\n) -> Callable[IN, Awaitable[OUT]]:\r\n    @wraps(func)\r\n    async def wrapper(*args: IN.args, **kwargs: IN.kwargs) -> OUT:\r\n        try:\r\n            LOGGER.debug(f"Executando a fun\xc3\xa7\xc3\xa3o {func.__name__} ")\r\n            result: OUT = await func(*args, **kwargs)\r\n            LOGGER.debug(f"Fun\xc3\xa7\xc3\xa3o {func.__name__} executada com sucesso")\r\n        except HTTPException as e:\r\n            LOGGER.warning(\r\n                f"Erro na fun\xc3\xa7\xc3\xa3o {func.__name__}: {e}",\r\n                extra={\r\n                    "func_name": func.__name__,\r\n                },\r\n            )\r\n            raise e from e\r\n        except Exception as e:\r\n            LOGGER.exception(\r\n                f"Erro na fun\xc3\xa7\xc3\xa3o {func.__name__}: {e}",\r\n                extra={\r\n                    "func_name": func.__name__,\r\n                },\r\n            )\r\n            raise HTTPException(\r\n                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,\r\n                detail=f"Erro na fun\xc3\xa7\xc3\xa3o {func.__name__}: {e}",\r\n            ) from e\r\n        return result\r\n\r\n    wrapper.__name__ = func.__name__\r\n\r\n    return wrapper\r\n')
    __scriptmerge_write_module('routes/levels.py', b'from database import AsyncSessionDep\r\nfrom fastapi import APIRouter\r\nfrom schemas.levels import Level, LevelCreate, LevelUpdate\r\nfrom schemas.message import Message\r\nfrom utils.aio_helpers import create_item, delete_item, get_all_items, update_item\r\n\r\nrouter = APIRouter(prefix="/levels", tags=["level"])\r\n\r\n\r\n@router.post("/")\r\nasync def create_level(level: LevelCreate, session: AsyncSessionDep) -> Level:\r\n    return await create_item(session, Level, level.model_dump())\r\n\r\n\r\n@router.get("/")\r\nasync def get_levels(session: AsyncSessionDep) -> list[Level]:\r\n    return list(await get_all_items(session=session, model=Level))\r\n\r\n\r\n@router.put("/")\r\nasync def atualizar_level(level: LevelUpdate, session: AsyncSessionDep) -> Level:\r\n    return await update_item(session, Level, level.model_dump())\r\n\r\n\r\n@router.delete("/")\r\nasync def deletar_level(id: int, session: AsyncSessionDep) -> Message:  # noqa: A002\r\n    await delete_item(session, Level, id)\r\n    return Message(status="sucess", message=f"Level {id= } deletado com sucesso")\r\n')
    __scriptmerge_write_module('schemas/message.py', b'from pydantic import BaseModel\r\n\r\n\r\nclass Message(BaseModel):\r\n    status: str\r\n    message: str\r\n')
    __scriptmerge_write_module('routes/token.py', b'from database import AsyncSessionDep\r\nfrom fastapi import APIRouter\r\nfrom schemas.token import TokenCreate, TokenData, TokenUpdate\r\nfrom utils.aio_helpers import create_item, update_item\r\n\r\nrouter = APIRouter(prefix="/token", tags=["token"])\r\n\r\n\r\n@router.post("/")\r\nasync def create_token(token: TokenCreate, session: AsyncSessionDep) -> TokenData:\r\n    return await create_item(session=session, model=TokenData, data=token.model_dump())\r\n\r\n\r\n@router.put("/")\r\nasync def update_token(token: TokenUpdate, session: AsyncSessionDep) -> TokenData:\r\n    return await update_item(session, TokenData, token.model_dump())\r\n')
    from typing import Any, Literal
    
    from fastapi import FastAPI
    from fastapi.openapi.utils import get_openapi
    from routes import atividade, levels, token
    from uvicorn import run
    
    app = FastAPI()
    app.include_router(token.router)
    app.include_router(levels.router)
    app.include_router(atividade.router)
    
    
    def custom_openapi() -> dict[str, Any]:
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema: dict[str, Any] = get_openapi(
            title="Artemiro BACKEND",
            version="0.0.5",
            summary="Sistema de monitoramento dos jogadores",
            description="O acesso desta api eh para jogadores",
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
    