from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_root():
    response = {"message": "Welcome to LuckyPay!!!"}
    return response
