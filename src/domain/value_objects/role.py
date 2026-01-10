from dataclasses import dataclass

from domain.exceptions import InvalidValue


@dataclass(frozen=True, slots=True)
class RoleName:
    value: str

    def __post_init__(self):
        if not self.value:
            raise InvalidValue("Role name is required")
        
    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class RoleDescription:
    value: str | None
        
    def __str__(self) -> str:
        return str(self.value)
    

@dataclass(frozen=True, slots=True)
class Permission:
    value: str

    def __post_init__(self):
        if not self.value:
            raise InvalidValue("Permission is requried")

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Permission) and self.value == other.value

    def __str__(self) -> str:
        return str(self.value)