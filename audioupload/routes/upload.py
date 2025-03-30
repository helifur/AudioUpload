import os
from typing import Annotated, Optional

import aiofiles
from fastapi import (
    APIRouter,
    Depends,
    Header,
    HTTPException,
    UploadFile,
    status,
)

from audioupload.core.security import (
    authenticate_user,
    get_user_yandex_data_from_token,
)
from audioupload.repository.audiofile import AudioFileRepository
from audioupload.repository.user import UserRepository

upload_router = APIRouter()


@upload_router.post("/upload")
async def upload_file(
    token: Annotated[str | None, Header(), Depends(authenticate_user)],
    file: UploadFile,
    filename: Optional[str] = None,
):

    if not file.content_type.startswith("audio"):
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Invalid file format!"
        )

    user_data = await get_user_yandex_data_from_token(token)

    UPLOAD_DIR = f"audioupload/static/audiofiles/{user_data.id}"
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_format = file.filename.split(".")[1]
    candidate_name = (
        file.filename
        if not filename
        else ".".join([filename.split(".")[0], file_format])
    )

    file_path = os.path.join(UPLOAD_DIR, candidate_name)

    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    owner = await UserRepository.get_one_or_none(yandex_user_id=user_data.id)
    await AudioFileRepository.insert(
        path="/".join([UPLOAD_DIR, candidate_name]), owner_id=owner["user_id"]
    )

    return {"file content type": file.content_type}
