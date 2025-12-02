from typing import Optional
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, HttpUrl, Field


class LinkCreateSchema(BaseModel):
    owner_id: UUID | None
    base_url: HttpUrl
    expires_at: Optional[datetime] = None
    redirect_limit: Optional[int] = Field(None, gt=0)

class LinkUpdateSchema(LinkCreateSchema):
    owner_id: Optional[UUID] = None
    base_url: Optional[HttpUrl] = None
    expires_at: Optional[datetime] = None

class LinkSchema(LinkCreateSchema):
    url_id: UUID
    base_url: HttpUrl
    # short_url: str
    suffix: str
    times_used: int
    is_active: bool

class LinkListSchema(BaseModel):
    data: list[LinkSchema]