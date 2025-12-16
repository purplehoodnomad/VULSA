from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.databases.postgresql.models import LinkORM

from domain.link.repository import AbstractLinkRepository
from domain.link.entity import Link
from domain.value_objects.common import LinkId
from domain.value_objects.link import Short
from domain.link.repository import LinkFilterDto
from domain.link.exceptions import LinkDoesNotExist


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
    
    async def list(self,
        filter: LinkFilterDto
    ) -> list[Link]:
        expression = []

        if filter.user is not None:
            expression.append(LinkORM.user_id == filter.user)
        if filter.older_than is not None:
            expression.append(LinkORM.created_at < filter.older_than)
        if filter.newer_than is not None:
            expression.append(LinkORM.created_at > filter.newer_than)
        if filter.active_status is not None:
            expression.append(LinkORM.is_active == filter.active_status)
        if filter.has_expiration_date is not None:
            if filter.has_expiration_date:
                expression.append(LinkORM.expires_at.isnot(None))
            else:
                expression.append(LinkORM.expires_at.is_(None))
        if filter.has_redirect_limit is not None:
            if filter.has_redirect_limit:
                expression.append(LinkORM.redirect_limit.isnot(None))
            else:
                expression.append(LinkORM.redirect_limit.is_(None))

        query = select(LinkORM).where(*expression).offset(filter.offset).limit(filter.limit)

        result = await self._session.execute(query)
        scalars = result.scalars().all()

        return [scalar.to_entity() for scalar in scalars]
