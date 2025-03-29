from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile

from audioupload.core.security import authenticate_user, oauth2_scheme

upload_router = APIRouter()


@upload_router.post("/files/")
async def create_file(file: Annotated[bytes, File(), Depends(oauth2_scheme)]):
    return {"file_size": len(file)}


@upload_router.post("/upload/")
async def upload_file(file: Annotated[UploadFile, Depends(oauth2_scheme)]):
    return {"filename": file.filename}
