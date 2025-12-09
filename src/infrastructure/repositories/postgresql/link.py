from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from databases.postgresql.models import LinkORM

from domain.link.repository import AbstractLinkRepository
from domain.link.entity import Link
from domain.common.value_objects import LinkId
from domain.link.exceptions import LinkDoesNotExist
from src.domain.link.value_objects import Short


class PostgresLinkRepository(AbstractLinkRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session
    
    async def create(self, entity: Link) -> Link:
        link_orm = LinkORM.from_entity(entity)

        self._session.add(link_orm)
        await self._session.flush()
        
        return link_orm.to_entity()


    async def get(self, link_id: LinkId) -> Link:
        link_orm = await self._session.get(LinkORM, link_id.value)

        if link_orm is None:
            raise LinkDoesNotExist()

        return link_orm.to_entity()


    async def get_by_short(self, short: Short) -> Link:
        statement = select(LinkORM).where(LinkORM.short == short.value)
        result = await self._session.execute(statement)
        link_orm = result.scalar_one_or_none()

        if link_orm is None:
            raise LinkDoesNotExist()
        
        return link_orm.to_entity()
