from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlmodel import Session

from api.models.prize import PrizeBody
from api.database.connection import get_db
from api.configuration.security import get_current_user
from api.database.repository import prize as prize_repo

router = APIRouter()


@router.post("", status_code=201)
def create_prize(
    prize: PrizeBody,
    db: Annotated[Session, Depends(get_db)],
    user_info: Annotated[any, Depends(get_current_user)],
    number: str = None,
    is_autoassigned: bool = False,
):
    
    if "admin" not in user_info["roles"]:
        raise HTTPException(403, "You're not allowed to access this resource!")

    new_prize = prize_repo.create_prize(db, prize, number, is_autoassigned)
    return {"message": "SUCESS_REGISTER_PRIZE", "data": new_prize}


@router.patch("/raffle", status_code=200)
def raffle_prize(prize_id: int, db: Annotated[Session, Depends(get_db)], number: str):
    new_prize = prize_repo.raffle_prize(db, prize_id, number)
    return {"message": "SUCESS_REGISTER_PRIZE", "data": new_prize}
