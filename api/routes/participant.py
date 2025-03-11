from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlmodel import Session


from api.models.participant import ParticipantBody, CreateParticipantBody

from api.database.connection import get_db
from api.configuration.security import finish_registration, get_current_user
from api.database.repository import participant as participant_repo

router = APIRouter()


@router.post("", status_code=201)
def finish_registration(
    participantBody: ParticipantBody,
    db: Annotated[Session, Depends(get_db)],
    user_info: Annotated[any, Depends(finish_registration)],
):
    new_participant = participant_repo.finish_participant_registration(
        db, participantBody, user_info
    )
    return {"message": "SUCESS_FINISH_REGISTRATION", "data": new_participant}

@router.post("create", status_code=201)
def create_participant(
    participant_body: CreateParticipantBody,
    db: Annotated[Session, Depends(get_db)]
):
    new_participant = participant_repo.create_participant(
        db, participant_body
    )
    return {"message": "SUCESS_FINISH_REGISTRATION", "data": new_participant}


@router.patch("", status_code=200)
def turn_admin(
    email: str,
    db: Annotated[Session, Depends(get_db)],
    user_info: Annotated[any, Depends(get_current_user)],
):
    
    if "admin" not in user_info["roles"]:
        raise HTTPException(403, "Only admins can turn another users as admin!")

    participant_repo.turn_admin(
        db, email, user_info
    )
    return {"message": "SUCESS_TURN_ADMIN"}
