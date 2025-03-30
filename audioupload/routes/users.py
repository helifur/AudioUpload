from typing import Annotated

from fastapi import APIRouter, Depends, Header

from audioupload.core.security import (
    authenticate_user,
    get_user_local_data_from_token,
)
from audioupload.repository.audiofile import AudioFileRepository

user_router = APIRouter()


@user_router.get("/user")
async def get_files(
    token: Annotated[str | None, Header(), Depends(authenticate_user)],
):
    user = await get_user_local_data_from_token(token)
    files = await AudioFileRepository.get_all(
        owner_id=user["user_id"], limit=0, skip=0
    )

    return {
        "user_id": user["user_id"],
        "name": user["first_name"],
        "files": [elem["path"].split("/")[-1] for elem in files],
    }
