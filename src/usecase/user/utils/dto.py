from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from domain.user.entity import User

from api.v1.user.schemas import UserSchema, UserCreateSchema, UserDeleteSchema


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
    
    def to_schema(self) -> UserSchema:
        return UserSchema(
            user_id=self.user_id,
            email=self.email,
            role=self.role,
            created_at=self.created_at
        )


@dataclass(slots=True)
class UserCreateDTO:
    email: str
    password: str
    role: str

    @staticmethod
    def from_schema(schema: UserCreateSchema) -> "UserCreateDTO":
        return UserCreateDTO(
            email=str(schema.email),
            password=schema.password,
            role=schema.role
        )


@dataclass(slots=True)
class UserDeleteDTO:
    user_id: UUID
    email: str
    password: str

    @staticmethod
    def from_schema(user_id: UUID, schema: UserDeleteSchema) -> "UserDeleteDTO":
        return UserDeleteDTO(
            user_id=user_id,
            email=str(schema.email),
            password=schema.password,
        )