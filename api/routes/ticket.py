from fastapi import APIRouter, Depends
from typing import Annotated
from sqlmodel import Session

from api.database.connection import get_db
from api.database.repository import tickets as ticket_repo
from api.configuration.security import get_current_user

router = APIRouter()


@router.patch("/sell", status_code=200)
def raffle_prize(
    raffle_id: int,
    ticket_qtd: int,
    db: Annotated[Session, Depends(get_db)],
    user_info: Annotated[any, Depends(get_current_user)],
):
    tickets = ticket_repo.sell_tickets(db, raffle_id, ticket_qtd, user_info)
    return {"message": "SUCESS_selling_all_tickets", "data": [tickets]}
