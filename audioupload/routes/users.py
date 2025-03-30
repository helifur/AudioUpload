from pathlib import Path
from typing import Annotated

import aiofiles.os as aios
from fastapi import APIRouter, Depends, Header, HTTPException, status

from audioupload.core.security import (
    authenticate_user,
    get_user_local_data_from_token,
    get_user_yandex_data_from_token,
)
from audioupload.repository.audiofile import AudioFileRepository
from audioupload.repository.role import RoleRepository
from audioupload.repository.user import UserRepository
from audioupload.schemas.user import UserSchema

user_router = APIRouter()


@user_router.get("/user")
async def get_user(
    token: Annotated[str | None, Header(), Depends(authenticate_user)],
):
    user = await get_user_local_data_from_token(token)
    files = await AudioFileRepository.get_all(
        owner_id=user["user_id"], limit=0, skip=0
    )

    return {
        "yandex_user_id": user["yandex_user_id"],
        "name": user["first_name"],
        "filenames": [elem["path"].split("/")[-1] for elem in files],
        "filepaths": [elem["path"] for elem in files],
    }


@user_router.patch("/user_edit")
async def edit_user(
    token: Annotated[str | None, Header(), Depends(authenticate_user)],
    user: UserSchema,
):
    user_data = await get_user_local_data_from_token(token)
    stored_user_model = UserSchema(**user_data)
    update_data = user.dict(exclude_unset=True)
    updated_user = stored_user_model.copy(update=update_data)

    user_role = await RoleRepository.get_one_or_none(role_id=user_data.role_id)

    if (
        user_role.name != "superuser"
        and user_data.role_id != updated_user.role_id
    ) or user_data.user_id != updated_user.user_id:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "Modified prohibited fields!"
        )

    res = await UserRepository.update(
        id_=user_data.user_id, **updated_user.dict()
    )

    return res


@user_router.delete("/user_delete")
async def delete_user(
    token: Annotated[str | None, Header(), Depends(authenticate_user)],
    candidate_yandex_id: str,
):
    user_data = await get_user_local_data_from_token(token)
    user_role = await RoleRepository.get_one_or_none(role_id=user_data.role_id)

    if user_role.name != "superuser":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not allowed!")

    if not await UserRepository.get_one_or_none(
        yandex_user_id=candidate_yandex_id
    ):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found!")

    candidate_data = await get_user_yandex_data_from_token(token)
    CANDIDATE_DIR = Path(f"audioupload/static/audiofiles/{candidate_data.id}")

    async def delete_recursive(p: Path):
        if await aios.path.isdir(p):
            for entry in await aios.listdir(p):
                await delete_recursive(p / entry)
            await aios.rmdir(p)
        else:
            await aios.remove(p)

    try:
        await delete_recursive(CANDIDATE_DIR)
    except FileNotFoundError:
        pass

    return await UserRepository.delete(candidate_yandex_id)
