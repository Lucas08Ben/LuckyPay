from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

from api.models.raffle import Raffle
from api.models.prize import Prize
from api.models.participant import Participant


class Ticket(SQLModel, table=True):
    __tablename__ = "ticket"

    id: int = Field(primary_key=True)
    raffle_id: int = Field(foreign_key="raffle.id")
    prize_id: int | None = Field(default=None, foreign_key="prize.id")
    participant_id: int | None = Field(default=None, foreign_key="participant.id")
    number: str
    purchased_in: datetime | None
    is_drawn: bool = False
    raffle: Raffle = Relationship()
    prize: Prize = Relationship()
    participant: Participant = Relationship()


class TicketBody(SQLModel):
    id: int = Field(primary_key=True)
    raffle_id: int
    prize_id: int | None
    participant: int | None
    number: str
    purchased_in: datetime | None

    model_config = {"from_attributes": True, "use_enum_values": True}
