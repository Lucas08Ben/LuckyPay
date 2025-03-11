from sqlmodel import Session, select, func
from fastapi import HTTPException
from datetime import datetime

from api.models.raffle import Raffle
from api.models.ticket import Ticket
from api.models.prize import Prize
from api.models.participant import Participant


def create_tickets_of_raffle(db: Session, raffle: Raffle):
    num_digits = len(str(raffle.total_tickets))

    batch_size = 100000
    for i in range(0, raffle.total_tickets, batch_size):
        print(f"total of tickets writed: {i:,}")
        tickets = [
            {"raffle_id": raffle.id, "number": f"{j:0{num_digits}d}"}
            for j in range(i + 1, min(i + batch_size + 1, raffle.total_tickets + 1))
        ]
        db.bulk_insert_mappings(Ticket, tickets)
        db.commit()  # Commit a cada lote

    print(f"total of tickets writed: {raffle.total_tickets:,}")


def assign_ticket_to_prize_auto(db: Session, prize: Prize):
    query = (
        select(Ticket)
        .where(Ticket.raffle_id == prize.raffle_id)
        .where(Ticket.prize_id.is_(None))
        .where(Ticket.is_drawn.is_(False))
        .order_by(func.random())
        .limit(1)
    )

    ticket = db.exec(query).first()

    if not ticket:
        raise HTTPException(404, "No Tickets found")

    if ticket.participant_id:
        raise HTTPException(403, "Ticket already taken by participant")

    ticket.prize_id = prize.id

    db.commit()
    db.refresh(ticket)


def assign_ticket_to_prize(db: Session, prize: Prize, number: str):
    query = (
        select(Ticket)
        .where(Ticket.raffle_id == prize.raffle_id)
        .where(Ticket.number == number)
        .limit(1)
        .order_by(func.random())
    )

    ticket = db.exec(query).first()

    if ticket is None:
        raise HTTPException(404, "No Tickets found")

    if ticket.participant_id:
        raise HTTPException(403, "Ticket already taken by participant")

    if ticket.prize_id:
        raise HTTPException(403, "Ticket already with prize")

    ticket.prize_id = prize.id
    db.commit()
    db.refresh(ticket)


def raffle_ticket(db: Session, prize: Prize, number: str):
    query = (
        select(Ticket)
        .where(Ticket.raffle_id == prize.raffle_id)
        .where(Ticket.number == number)
    )

    ticket = db.exec(query).first()

    if ticket is None:
        raise HTTPException(404, "Ticket not found!")

    if not ticket.participant_id:
        raise HTTPException(409, "This ticket was not bought!")

    ticket.is_drawn = True
    db.commit()
    db.refresh(ticket)


def sell_tickets(db: Session, raffle_id: int, tickets_qtd: int, user_info):
    user_id = db.exec(
        select(Participant.id).where(Participant.email == user_info["email"])
    ).first()

    amount_of_available_tickets = db.exec(
        select(func.count())
        .filter(Ticket.raffle_id == raffle_id)
        .filter(Ticket.participant_id.is_(None))
    ).first()

    if tickets_qtd > amount_of_available_tickets:
        raise HTTPException(
            409,
            f"It seems that there are not many tickets available, please select a number smaller than {amount_of_available_tickets}",
        )

    query = (
        select(Ticket)
        .where(Ticket.raffle_id == raffle_id)
        .order_by(func.random())
        .limit(tickets_qtd)
    )

    tickets = db.exec(query).fetchall()

    for ticket in tickets:
        ticket.participant_id = user_id
        ticket.purchased_in = datetime.now()

    db.commit()
    for product in tickets:
        db.refresh(product)
    return tickets
