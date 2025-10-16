from database import AsyncSessionDep
from fastapi import APIRouter
from schemas.token import TokenCreate, TokenData, TokenUpdate
from utils.aio_helpers import create_item, update_item

router = APIRouter(prefix="/token", tags=["token"])


@router.post("/")
async def create_token(token: TokenCreate, session: AsyncSessionDep) -> TokenData:
    return await create_item(session=session, model=TokenData, data=token.model_dump())


@router.put("/")
async def update_token(token: TokenUpdate, session: AsyncSessionDep) -> TokenData:
    return await update_item(session, TokenData, token.model_dump())
