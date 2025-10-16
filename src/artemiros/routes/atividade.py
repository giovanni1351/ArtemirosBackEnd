from database import AsyncSessionDep
from fastapi import APIRouter
from schemas.atividade import Atividade, AtividadeCreate
from utils.aio_helpers import create_item

router = APIRouter(prefix="/atividade", tags=["atividade"])


@router.post("/")
async def create_atividade(
    atividade: AtividadeCreate, session: AsyncSessionDep
) -> Atividade:
    return await create_item(session, Atividade, atividade.model_dump())
