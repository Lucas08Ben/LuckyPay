from sqlmodel import Session, select
from fastapi import HTTPException

from api.models.participant import Participant, ParticipantBody, CreateParticipantBody
from api.configuration.security import keycloak_admin
from api.configuration.settings import envs


def finish_participant_registration(
    db: Session, participant: ParticipantBody, user_info
) -> Participant:
    new_participant = Participant(**participant.model_dump())
    new_participant.name = user_info["name"]
    new_participant.email = user_info["email"]

    db.add(new_participant)
    db.commit()
    db.refresh(new_participant)
    return new_participant

def create_participant(db: Session, participant_body: CreateParticipantBody):

    payload = {
        "email": participant_body.email,
        "username": participant_body.email,
        "enabled": True,
        "firstName": participant_body.first_name,
        "lastName": participant_body.last_name,
        "attributes": {"registration_completed": True},
        "credentials": [
            {
                "type": "password",
                "value": participant_body.password
            }
        ]
    }

    keycloak_admin.create_user(payload=payload, exist_ok=False)


    


def turn_admin(db: Session, email: str, user_info) -> Participant:
    participant = db.exec(
        select(Participant).where(Participant.email == email)
    ).first()

    if participant is None:
        raise HTTPException(404, "Participant not found")
    user_id = keycloak_admin.get_user_id(participant.email)
    client_id = keycloak_admin.get_client_id(envs.CLIENT_ID)
    test = keycloak_admin.assign_client_role(user_id=user_id, client_id=client_id, roles="admin")
    print(test)
