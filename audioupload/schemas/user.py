from pydantic import BaseModel


class UserSchema(BaseModel):
    user_id: int | None = None
    yandex_user_id: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    role_id: int = 0
