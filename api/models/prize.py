from sqlmodel import SQLModel, Field, TEXT, Relationship
from datetime import datetime

from api.models.raffle import Raffle


class Prize(SQLModel, table=True):
    __tablename__ = "prize"

    id: int = Field(primary_key=True)
    raffle_id: int = Field(foreign_key="raffle.id")
    name: str
    description: str = Field(sa_type=TEXT)
    is_main: bool
    drawn_at: datetime | None = None
    raffle: Raffle = Relationship()


class PrizeBody(SQLModel):
    raffle_id: int
    name: str
    description: str = Field(sa_type=TEXT)
    is_main: bool
