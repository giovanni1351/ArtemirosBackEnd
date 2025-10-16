from database import AsyncSessionDep
from fastapi import APIRouter
from schemas.levels import Level, LevelCreate, LevelUpdate
from schemas.message import Message
from utils.aio_helpers import create_item, delete_item, get_all_items, update_item

router = APIRouter(prefix="/levels", tags=["level"])


@router.post("/")
async def create_level(level: LevelCreate, session: AsyncSessionDep) -> Level:
    return await create_item(session, Level, level.model_dump())


@router.get("/")
async def get_levels(session: AsyncSessionDep) -> list[Level]:
    return list(await get_all_items(session=session, model=Level))


@router.put("/")
async def atualizar_level(level: LevelUpdate, session: AsyncSessionDep) -> Level:
    return await update_item(session, Level, level.model_dump())


@router.delete("/")
async def deletar_level(id: int, session: AsyncSessionDep) -> Message:  # noqa: A002
    await delete_item(session, Level, id)
    return Message(status="sucess", message=f"Level {id= } deletado com sucesso")
