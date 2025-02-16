from sqlmodel import Session, select
from fastapi import HTTPException

from api.models.prize import Prize, PrizeBody
from api.database.repository import tickets
from datetime import datetime


def create_prize(
    db: Session, prize: PrizeBody, number: str, is_autoassigned=False
) -> Prize:
    new_prize = Prize(**prize.model_dump())

    db.add(new_prize)
    db.commit()
    db.refresh(new_prize)

    if is_autoassigned:
        if not number:
            tickets.assign_ticket_to_prize_auto(db, new_prize)
        else:
            tickets.assign_ticket_to_prize(db, new_prize, number)

    return new_prize


def raffle_prize(db: Session, prize_id: int, number: str) -> Prize:
    query = select(Prize).where(Prize.id == prize_id)
    prize = db.exec(query).first()

    if prize is None:
        raise HTTPException(404, "Prize not found")

    tickets.raffle_ticket(db, prize, number)

    prize.down_at = datetime.now()

    db.commit()
    db.refresh(prize)

    return prize
