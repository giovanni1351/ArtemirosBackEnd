from pydantic import BaseModel


class Message(BaseModel):
    status: str
    message: str
