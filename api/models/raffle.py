from sqlmodel import SQLModel, Field, TEXT
from datetime import datetime


class Raffle(SQLModel, table=True):
    __tablename__ = "raffle"

    id: int = Field(primary_key=True)
    edition: int = Field(unique=True)
    started_at: datetime
    finished_at: datetime
    total_tickets: int
    description: str = Field(sa_type=TEXT)


class RaffleBody(SQLModel):
    edition: int
    started_at: datetime
    finished_at: datetime
    total_tickets: int
    description: str

    model_config = {"from_attributes": True, "use_enum_values": True}
