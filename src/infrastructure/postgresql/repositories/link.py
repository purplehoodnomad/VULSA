from datetime import datetime
from typing import Optional

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from infrastructure.postgresql.models import LinkORM
from infrastructure.postgresql.exceptions import handle_unique_integrity_error

from domain.link.repository import AbstractLinkRepository

from domain.link.entity import Link
from domain.link.exceptions import ShortLinkNotFound

from domain.value_objects.common import UserId
from domain.value_objects.link import Short


class PostgresLinkRepository(AbstractLinkRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session
    

    async def create(self, entity: Link) -> Link:
        link_orm = LinkORM.from_entity(entity)

        self._session.add(link_orm)
        try:
            await self._session.flush()
        except IntegrityError as e:
            handle_unique_integrity_error(e)
        
        return link_orm.to_entity()


    async def update(self, entity: Link) -> Link:
        link_orm = await self._session.get(LinkORM, entity.link_id.value)
        if link_orm is None:
            raise ShortLinkNotFound()
        
        link_orm.user_id = entity.user_id.value
        link_orm.long = entity.long.value
        link_orm.short = entity.short.value
        link_orm.is_active = entity.is_active
        link_orm.redirect_limit = entity.redirect_limit.value if entity.redirect_limit is not None else None
        link_orm.expires_at = entity.expires_at
        link_orm.times_used = entity.times_used

        try:
            await self._session.flush()
        except IntegrityError as e:
            handle_unique_integrity_error(e)
        
        return link_orm.to_entity()


    async def delete(self, entity: Link) -> None:
        stmt = delete(LinkORM).where(LinkORM.id == entity.link_id.value)
        await self._session.execute(stmt)


    async def get_by_short(self, short: Short) -> Link:
        statement = select(LinkORM).where(LinkORM.short == short.value)
        result = await self._session.execute(statement)
        link_orm = result.scalar_one_or_none()

        if link_orm is None:
            raise ShortLinkNotFound()
        
        return link_orm.to_entity()
    

    async def is_short_taken(self, short: Short) -> bool:
        statement = select(LinkORM).where(LinkORM.short == short.value)
        result = await self._session.execute(statement)
        link_orm = result.scalar_one_or_none()

        return link_orm is not None


    async def list(self,
        *,
        offset: int,
        limit: int,
        user_id: Optional[UserId] = None,
        older_than: Optional[datetime] = None,
        newer_than: Optional[datetime] = None,
        active_status: Optional[bool] = None,
        has_expiration_date: Optional[bool] = None,
        has_redirect_limit: Optional[bool] = None,
    ) -> list[Link]:
        expression = []

        if user_id is not None:
            expression.append(LinkORM.user_id == user_id.value)
        if older_than is not None:
            expression.append(LinkORM.created_at < older_than)
        if newer_than is not None:
            expression.append(LinkORM.created_at > newer_than)
        if active_status is not None:
            expression.append(LinkORM.is_active == active_status)
        if has_expiration_date is not None:
            if has_expiration_date:
                expression.append(LinkORM.expires_at.isnot(None))
            else:
                expression.append(LinkORM.expires_at.is_(None))
        if has_redirect_limit is not None:
            if has_redirect_limit:
                expression.append(LinkORM.redirect_limit.isnot(None))
            else:
                expression.append(LinkORM.redirect_limit.is_(None))

        query = select(LinkORM).where(*expression).offset(offset).limit(limit)

        result = await self._session.execute(query)
        scalars = result.scalars().all()

        if not scalars:
            return []

        return [scalar.to_entity() for scalar in scalars]