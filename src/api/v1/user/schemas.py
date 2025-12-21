from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, model_validator

from utils.enums import UserStatus


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    password_repeated: str

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.password_repeated:
            raise ValueError("Passwords do not match")
        return self


class UserSchema(BaseModel):
    user_id: UUID
    email: EmailStr
    status: UserStatus
    created_at: datetime


class UserDeleteSchema(BaseModel):
    email: EmailStr
    password: str
    password_repeated: str

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.password_repeated:
            raise ValueError("Passwords do not match")
        return self