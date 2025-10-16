from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import (  # pyright: ignore[reportUnknownVariableType]
    Field,  # pyright: ignore[reportUnknownVariableType]
    Relationship,
    SQLModel,
)

if TYPE_CHECKING:
    from schemas.atividade import (
        Atividade,
    )


class LevelCreate(SQLModel):
    nome_level: str


class LevelUpdate(SQLModel):
    id: int
    nome_level: str


class Level(LevelCreate, table=True):
    id: int = Field(primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    atividades: list["Atividade"] = Relationship(back_populates="level")
