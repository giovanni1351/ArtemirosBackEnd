from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import (
    Field,  # pyright: ignore[reportUnknownVariableType]
    Relationship,
    SQLModel,
)

if TYPE_CHECKING:
    from schemas.atividade import Atividade


class TokenCreate(SQLModel):
    username: str | None = None


class TokenUpdate(SQLModel):
    id: UUID
    momento_fechamento: datetime | None


class TokenData(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default_factory=uuid4)
    momento_abertura: datetime = Field(default_factory=datetime.now)
    momento_fechamento: datetime | None = Field(default=None)
    atividades: list["Atividade"] = Relationship(back_populates="token")
