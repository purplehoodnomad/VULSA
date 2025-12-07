from uuid import UUID
from datetime import datetime, timezone
from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from databases.postgresql.models import LinkORM

from domain.link.repository import AbstractLinkRepository
from domain.link.entity import Link
from domain.link.exceptions import LinkDoesNotExist, ShortLinkAlreadyExists


class PostgresLinkRepository(AbstractLinkRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session
    
    async def create(self, entity: Link) -> Link:
        link_orm = LinkORM.from_entity(entity)

        self._session.add(link_orm)
        
        try:
            await self._session.flush()
        except IntegrityError:
            await self._session.rollback()
            raise ShortLinkAlreadyExists(link_orm.short)
        
        return link_orm.to_entity()


    # async def get(self, url_id: LinkId) -> Link:
    #     link = await self._session.get(Link, url_id)

    #     if link is None:
    #         raise LinkDoesNotExist()

    #     return link_to_dto(link)
