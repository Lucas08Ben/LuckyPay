from sqlmodel import Session

from api.models.raffle import RaffleBody, Raffle
from api.database.repository import tickets


def create_raffle(db: Session, raffle: RaffleBody) -> Raffle:
    new_raffle = Raffle(**raffle.model_dump())

    db.add(new_raffle)
    db.commit()
    db.refresh(new_raffle)

    tickets.create_tickets_of_raffle(db, new_raffle)
    return new_raffle
