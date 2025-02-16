from sqlmodel import SQLModel, Field, func
from datetime import datetime


class Participant(SQLModel, table=True):
    __tablename__ = "participant"

    id: int = Field(primary_key=True)
    name: str
    cpf: str = Field(unique=True)
    email: str = Field(unique=True)
    phone: str
    created_at: datetime = Field(default=func.now())
    is_active: bool = True


class ParticipantBody(SQLModel):
    __tablename__ = "participant"

    cpf: str
    phone: str
