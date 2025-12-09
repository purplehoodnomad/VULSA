from typing import Optional, Annotated
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, HttpUrl, Field, BeforeValidator

from config import MIN_SHORT_LINK_LENGTH, MAX_SHORT_LINK_LENGTH


def validate_short_link(value: Optional[str]) -> str | None:
    return None if value is None or len(value) < MIN_SHORT_LINK_LENGTH or len(value) > MAX_SHORT_LINK_LENGTH else value


class LinkCreateSchema(BaseModel):
    user_id: UUID
    long: HttpUrl
    short: Annotated[Optional[str], BeforeValidator(validate_short_link)]
    expires_at: Optional[datetime] = None
    redirect_limit: Optional[int] = Field(None, gt=0)


class LinkUpdateSchema(BaseModel):
    user_id: Optional[UUID] = None
    long: Optional[HttpUrl] = None
    expires_at: Optional[datetime] = None
    redirect_limit: Optional[int] = Field(None, gt=0)


class LinkSchema(BaseModel):
    link_id: UUID
    user_id: UUID
    long: str
    short: Optional[str]
    times_used: Optional[int]
    is_active: Optional[bool]
    expires_at: Optional[datetime]
    redirect_limit: Optional[int]
    created_at: Optional[datetime]


class LinkListSchema(BaseModel):
    data: list[LinkSchema]