from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.user.entity import User


@dataclass(slots=True)
class UserDTO:
    user_id: UUID
    email: str
    created_at: datetime
    role: str

    @staticmethod
    def from_entity(entity: User):
        return UserDTO(
            user_id=entity.user_id.value,
            email=entity.email.value,
            created_at=entity.created_at,
            role=entity.role.value
        )


@dataclass(slots=True)
class UserCreateDTO:
    email: str
    password: str
    role: str


@dataclass(slots=True)
class UserDeleteDTO:
    user_id: UUID
    email: str
    password: str