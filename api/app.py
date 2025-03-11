from fastapi import FastAPI

from api.routes import root, raffle, prize, participant, ticket


def get_app() -> FastAPI:
    app = FastAPI(
        title="LuckyPay API",
        description="API of the best raffle in Brazil",
        version="1.0.0",
    )

    app.include_router(root.router, tags=["Root"])
    app.include_router(raffle.router, prefix="/raffle", tags=["Raffle"])
    app.include_router(prize.router, prefix="/prize", tags=["Prize"])
    app.include_router(participant.router, prefix="/participant", tags=["Participant"])
    app.include_router(ticket.router, prefix="/ticket", tags=["Ticket"])

    return app
