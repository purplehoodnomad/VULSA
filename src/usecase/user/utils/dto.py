from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.user.entity import User
from domain.value_objects.user import Email, HashedPassword
from utils.enums import UserStatus


@dataclass(slots=True)
class UserDTO:
    user_id: UUID
    email: str
    created_at: datetime
    status: UserStatus

    @staticmethod
    def from_entity(entity: User):
        return UserDTO(
            user_id=entity.user_id.value,
            email=entity.email.value,
            created_at=entity.created_at,
            status=entity.status
        )


@dataclass(slots=True)
class UserCreateDTO:
    email: str
    password: str

    def to_entity(self):
        "Converts dto into User entity with empty hashed password and USER status"
        return User.create(
                email=Email(self.email),
                hashed_password=HashedPassword(""),
                status=UserStatus.USER
            )

@dataclass(slots=True)
class UserDeleteDTO:
    user_id: UUID
    email: str
    password: str