from pydantic import BaseModel


class EditPermissionSchema(BaseModel):
    role: str
    permission: str

class RoleSchema(BaseModel):
    role_name: str
    description: str | None
    permissions: list[str]
