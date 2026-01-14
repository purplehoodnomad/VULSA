from dataclasses import dataclass
from uuid import UUID

from domain.role.entity import Role
from api.v1.admin.schemas import RoleSchema, EditPermissionSchema


@dataclass(frozen=True, slots=True)
class RoleDTO:
    name: str
    description: str | None
    permissions: list[str]

    @staticmethod
    def from_entity(entity: Role) -> "RoleDTO":
        return RoleDTO(
            name=entity.name.value,
            description=entity.description.value,
            permissions=[str(permission.value) for permission in entity.permissions]
        )
    
    def to_schema(self) -> RoleSchema:
        return RoleSchema(
            role_name=self.name,
            description=self.description,
            permissions=self.permissions
        )
    
@dataclass(frozen=True, slots=True)
class EditPermissionDTO:
    user_id: UUID
    role: str
    permission: str

    @staticmethod
    def from_schema(user_id: UUID, schema: EditPermissionSchema) -> "EditPermissionDTO":
        return EditPermissionDTO(
            user_id=user_id,
            role=schema.role,
            permission=schema.permission
        )