from datetime import datetime

from sqlmodel import (  # pyright: ignore[reportUnknownVariableType]
    Field,  # pyright: ignore[reportUnknownVariableType]
    Relationship,
    SQLModel,
)

from schemas.levels import Level
from schemas.token import TokenData


class AtividadeCreate(SQLModel):
    id_level: int = Field(foreign_key="level.id")
    id_token: int = Field(foreign_key="tokendata.id")
    atividade: str


class Atividade(AtividadeCreate, table=True):
    id: int = Field(primary_key=True)
    level: Level = Relationship(back_populates="atividades")
    token: TokenData = Relationship(back_populates="atividades")
    created_at: datetime
