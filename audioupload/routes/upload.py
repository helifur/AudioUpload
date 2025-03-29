from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile

upload_router = APIRouter()


@upload_router.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@upload_router.post("/upload/")
async def upload_file(file: UploadFile):
    return {"filename": file.filename}
