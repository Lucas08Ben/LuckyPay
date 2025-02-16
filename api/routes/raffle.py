from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlmodel import Session

from api.models.raffle import RaffleBody
from api.database.connection import get_db
from api.configuration.security import get_current_user
from api.database.repository import raffle as raffle_repo

router = APIRouter()


@router.post("", status_code=201)
def create_raffle(
    raffle: RaffleBody,
    db: Annotated[Session, Depends(get_db)],
    user_info: Annotated[any, Depends(get_current_user)],
):
    

    if "admin" not in user_info["roles"]:
        raise HTTPException(403, "You're not allowed to access this resource!")

    new_raffle = raffle_repo.create_raffle(db, raffle)
    return {"message": "SUCESS_REGISTER_RAFFLE", "data": new_raffle}
