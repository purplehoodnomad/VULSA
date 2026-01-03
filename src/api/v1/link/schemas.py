from typing import Optional, Annotated
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, HttpUrl, Field, BeforeValidator

from config.config import MIN_SHORT_LINK_LENGTH, MAX_SHORT_LINK_LENGTH


class LinkCreateSchema(BaseModel):
    long: HttpUrl
    short: Optional[str] = None
    expires_at: Optional[datetime] = None
    redirect_limit: Optional[int] = Field(None, gt=0)


class LinkUpdateSchema(BaseModel):
    long: Optional[HttpUrl] = None
    new_short: Optional[str] = None
    expires_at: Optional[datetime] = Field(None, gt=0)
    redirect_limit: Optional[int] = None
    is_active: Optional[bool] = None


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


class LinkListQueryParams(BaseModel):
    offset: int = Field(0, ge=0)
    limit: int = Field(2, ge=1, le=100)
    older_than: Optional[datetime] = None
    newer_than: Optional[datetime] = None
    active_status: Optional[bool] = None
    has_expiration_date: Optional[bool] = None
    has_redirect_limit: Optional[bool] = None