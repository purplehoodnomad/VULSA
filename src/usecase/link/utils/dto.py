from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from uuid import UUID

from domain.link.entity import Link
from infrastructure.cache.entries.link import LinkCacheEntry
from domain.value_objects.common import UserId
from domain.value_objects.link import Short, Long, RedirectLimit, AnonymousEditKey
from usecase.common.actor import Actor

from api.v1.link.schemas import (
    LinkSchema, 
    SimpleLinkSchema, 
    LinkCreateSchema,
    LinkUpdateSchema,
    LinkListQueryParams,
    LinkStatsSchema,
)


@dataclass(slots=True)
class LinkDTO:
    link_id: UUID
    owner_id: UUID | str
    long: str
    short: str
    redirect_limit: Optional[int]
    expires_at: Optional[datetime]
    created_at: datetime
    times_used: int
    is_active: bool

    @staticmethod
    def from_entity(entity: Link):
        return LinkDTO(
            link_id=entity.link_id.value,
            owner_id=entity.owner_id.value,
            long=entity.long.value,
            short=entity.short.value,
            redirect_limit=entity.redirect_limit.value if entity.redirect_limit is not None else None,
            expires_at=entity.expires_at,
            created_at=entity.created_at,
            times_used=entity.times_used,
            is_active=entity.is_active
        )
    
    def to_schema(self) -> LinkSchema:
        return LinkSchema(
            link_id=self.link_id,
            owner_id=self.owner_id,
            long=self.long,
            short=self.short,
            is_active=self.is_active,
            expires_at=self.expires_at,
            redirect_limit=self.redirect_limit,
            created_at=self.created_at,
            times_used=self.times_used
        )


@dataclass(slots=True)
class SimpleLinkDTO:
    short: str
    long: str
    
    @staticmethod
    def from_cache_entry(entry: LinkCacheEntry) -> "SimpleLinkDTO":
        return SimpleLinkDTO(
            short=entry.short,
            long=entry.long
        )
    
    @staticmethod
    def from_entity(entity: Link) -> "SimpleLinkDTO":
        return SimpleLinkDTO(
            short=entity.short.value,
            long=entity.long.value
        )
    
    def to_schema(self) -> SimpleLinkSchema:
        return SimpleLinkSchema(
            short=self.short,
            long=self.long
        )


@dataclass(slots=True)
class LinkCreateDTO:
    actor: Actor
    long: str
    short: Optional[str]
    expires_at: Optional[datetime]
    redirect_limit: Optional[int]

    def to_entity(self):
        return Link.create(
                owner_id=UserId(self.actor.id) if self.actor.is_user() else AnonymousEditKey.generate(), # type: ignore
                long=Long(self.long),
                short=Short(self.short) if self.short else None,
                expires_at=self.expires_at,
                redirect_limit=RedirectLimit(self.redirect_limit)
            )
    
    @staticmethod
    def from_schema(actor: Actor, schema: LinkCreateSchema) -> "LinkCreateDTO":
        return LinkCreateDTO(
            actor=actor,
            long=str(schema.long),
            short = schema.short,
            expires_at=schema.expires_at,
            redirect_limit=schema.redirect_limit
        )


@dataclass(slots=True)
class LinkUpdateDTO:
    actor: Actor
    short: str
    long: Optional[str] = None
    new_short: Optional[str] = None
    expires_at: Optional[datetime] = None
    redirect_limit: Optional[int] = None
    is_active: Optional[bool] = None

    @staticmethod
    def from_schema(actor: Actor, short: str, schema: LinkUpdateSchema) -> "LinkUpdateDTO":  
        return LinkUpdateDTO(
            actor=actor,
            short=short,
            long=str(schema.long) if schema.long is not None else None,
            new_short=schema.new_short,
            expires_at=schema.expires_at,
            redirect_limit=schema.redirect_limit,
            is_active=schema.is_active
        )


@dataclass(slots=True)
class LinkFilterDto:
    offset: int
    limit: int
    user_id: Optional[UUID] = None
    edit_key: Optional[str] = None
    older_than: Optional[datetime] = None
    newer_than: Optional[datetime] = None
    active_status: Optional[bool] = None
    has_expiration_date: Optional[bool] = None
    has_redirect_limit: Optional[bool] = None

    @staticmethod
    def from_schema(actor: Actor, schema: LinkListQueryParams) -> "LinkFilterDto":
        return LinkFilterDto(
            offset=schema.offset,
            limit=schema.limit,
            user_id=actor.id if actor.is_user() else None, # type: ignore
            edit_key=actor.id if actor.is_anonymous() else None, # type: ignore
            older_than=schema.older_than,
            newer_than=schema.newer_than,
            active_status=schema.active_status,
            has_expiration_date=schema.has_expiration_date,
            has_redirect_limit=schema.has_redirect_limit
        )


@dataclass(slots=True, frozen=True)
class LinkTimeStatsDTO:
    link_id: UUID
    stats: dict[str, dict[str, int]] # date, hour, count

@dataclass(slots=True, frozen=True)
class LinkGeoStatsDTO:
    link_id: UUID
    stats: dict[str, int] # geo code, count

@dataclass(slots=True, frozen=True)
class LinkClientStatsDTO:
    link_id: UUID
    stats: dict[tuple[str, str], int] # (platform, client): count

@dataclass(slots=True, frozen=True)
class LinkStatsDTO:
    short: str
    click_count: int
    by_time: dict[str, dict[str, int]] # date, hour, count
    by_geo: dict[str, int] # geo code, count
    by_client: dict[tuple[str, str], int] # (platform, client): count

    @staticmethod
    def create(
        entity: Link,
        by_time: LinkTimeStatsDTO,
        by_geo: LinkGeoStatsDTO,
        by_client: LinkClientStatsDTO,
    ) -> "LinkStatsDTO":
        return LinkStatsDTO(
            short=entity.short.value,
            click_count=entity.times_used,
            by_time=by_time.stats,
            by_geo=by_geo.stats,
            by_client=by_client.stats
        )

    def to_schema(self) -> LinkStatsSchema:
        return LinkStatsSchema(
            short=self.short,
            click_count=self.click_count,
            by_time=self.by_time,
            by_geo=self.by_geo,
            by_client=self.by_client
        )