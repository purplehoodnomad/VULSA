from typing import Optional, Annotated
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr

from utils.enums import UserStatus


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str


class UserSchema(BaseModel):
    user_id: UUID
    email: EmailStr
    status: UserStatus
    created_at: datetime