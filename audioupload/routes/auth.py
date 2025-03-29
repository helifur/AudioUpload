from fastapi import APIRouter

auth_router = APIRouter()


@auth_router.post("/auth")
async def auth():
    pass
