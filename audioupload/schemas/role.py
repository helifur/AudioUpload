from pydantic import BaseModel


class RoleSchema(BaseModel):
    role_id: int | None = None
    name: str | None = None
