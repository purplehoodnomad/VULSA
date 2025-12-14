from abc import ABC, abstractmethod
from uuid import UUID
from datetime import datetime
from typing import Optional

from infrastructure.repositories.postgresql.uow import PostgreSQLLinkUoW

from domain.link.repository import LinkFilterDto

from ..common.mappers import link_entity_to_schema
from api.v1.link.schemas import LinkSchema, LinkListSchema


class GetLinkListUsecase(ABC):
    @abstractmethod
    async def execute(
        self,
        *,
        offset: int,
        limit: int,
        user: Optional[UUID],
        older_than: Optional[datetime],
        newer_than: Optional[datetime],
        active_status: Optional[bool],
        has_expiration_date: Optional[bool],
        has_redirect_limit: Optional[bool]
    ) -> LinkSchema:
        raise NotImplementedError
        

class GetLinkListUsecaseImpl(GetLinkListUsecase):
    def __init__(self, uow: PostgreSQLLinkUoW):
        self.uow = uow
    
    async def execute(
        self,
        *,
        offset: int,
        limit: int,
        user: Optional[UUID],
        older_than: Optional[datetime],
        newer_than: Optional[datetime],
        active_status: Optional[bool],
        has_expiration_date: Optional[bool],
        has_redirect_limit: Optional[bool]
    ) -> LinkListSchema:
        async with self.uow as uow:
            filter = LinkFilterDto(
                    offset=offset,
                    limit=limit,
                    user=user,
                    older_than=older_than,
                    newer_than=newer_than,
                    active_status=active_status,
                    has_expiration_date=has_expiration_date,
                    has_redirect_limit=has_redirect_limit
            )
            if uow.repository is not None:
                links = await uow.repository.list(filter)
            
            return LinkListSchema(data=[link_entity_to_schema(link) for link in links])