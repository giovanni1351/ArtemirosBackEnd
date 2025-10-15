
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas.token import TokenCreate, TokenData
from settings import SETTINGS
from database import AsyncSessionDep
router = APIRouter(prefix="/token", tags=["token"])

@router.post("/")
async def create_token(token: TokenCreate,session:AsyncSessionDep ) -> TokenData:
    
    