from dataclasses import dataclass

from domain.role.entity import Role


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