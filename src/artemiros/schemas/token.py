from datetime import datetime

from sqlmodel import Field, SQLModel  # pyright: ignore[reportUnknownVariableType]


class TokenCreate(SQLModel):
    username: str | None = None


class TokenData(SQLModel, table=True):
    id: int = Field(primary_key=True)
    momento_abertura: datetime = Field(default_factory=datetime.now)
    momento_fechamento: datetime | None = Field(default=None)
