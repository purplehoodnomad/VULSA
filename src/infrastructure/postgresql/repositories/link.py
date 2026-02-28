from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy import select, delete, and_, not_, or_, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from infrastructure.postgresql.models import LinkORM
from infrastructure.postgresql.exceptions import handle_unique_integrity_error

from domain.link.repository import AbstractLinkRepository

from domain.link.entity import Link
from domain.link.exceptions import ShortLinkNotFound, AnonymousSessionNotFound

from domain.value_objects.common import UserId
from domain.value_objects.link import AnonymousEditKey, Short


class PostgresLinkRepository(AbstractLinkRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session
    

    async def create(self, entity: Link) -> None:
        link_orm = LinkORM.from_entity(entity)

        self._session.add(link_orm)
        try:
            await self._session.flush()
        except IntegrityError as e:
            handle_unique_integrity_error(e)


    async def update(self, entity: Link) -> None:
        link_orm = await self._session.get(LinkORM, entity.link_id.value)
        if link_orm is None:
            raise ShortLinkNotFound()
        
        link_orm.update_from_entity(entity)
        try:
            await self._session.flush()
        except IntegrityError as e:
            handle_unique_integrity_error(e)


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
    

    async def get_by_edit_key(self, edit_key: AnonymousEditKey) -> Link:
        statement = select(LinkORM).where(LinkORM.edit_key == edit_key.value)
        result = await self._session.execute(statement)
        link_orm = result.scalar_one_or_none()

        if link_orm is None:
            raise AnonymousSessionNotFound()
        
        return link_orm.to_entity()
    

    async def is_short_taken(self, short: Short) -> bool:
        statement = select(LinkORM).where(LinkORM.short == short.value)
        result = await self._session.execute(statement)
        link_orm = result.scalar_one_or_none()

        return link_orm is not None


    async def list(self,
        *,
        offset: int = 0,
        limit: Optional[int] = None,
        user_id: Optional[UserId] = None,
        edit_key: Optional[AnonymousEditKey] = None,
        older_than: Optional[datetime] = None,
        newer_than: Optional[datetime] = None,
        active_status: Optional[bool] = None,
        has_expiration_date: Optional[bool] = None,
        has_redirect_limit: Optional[bool] = None,
    ) -> List[Link]:
        expression = []

        if user_id is not None:
            expression.append(LinkORM.user_id == user_id.value)
        if edit_key is not None:
            expression.append(LinkORM.edit_key == edit_key.value)
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

        query = select(LinkORM).where(*expression).offset(offset)
        if limit is not None:
            query = query.limit(limit)

        result = await self._session.execute(query)
        scalars = result.scalars().all()

        if not scalars:
            return []

        return [scalar.to_entity() for scalar in scalars]


    async def find_for_cleanup(self,
        *,
        last_used_before: datetime,
        include_expired: bool,
        include_limit_reached: bool,
        include_inactive: bool,
        limit: Optional[int] = None,
    ) -> List[Link]:
        conditions = []
        now = datetime.now(timezone.utc)

        date_condition = or_(
            LinkORM.last_used <= last_used_before,
            LinkORM.last_used.is_(None),
        )

        if include_expired:
            conditions.append(
                and_(
                    LinkORM.expires_at.isnot(None),
                    LinkORM.expires_at < now,
                )
            )

        if include_limit_reached:
            conditions.append(
                and_(
                    LinkORM.redirect_limit.isnot(None),
                    LinkORM.times_used >= LinkORM.redirect_limit,
                )
            )

        if include_inactive:
            conditions.append(
                LinkORM.is_active.is_(False)
            )
        
        if not conditions:
            return []
        
        query = select(LinkORM).where(
            and_(
                date_condition,
                or_(*conditions),
            )
        )
        if limit is not None:
            query = query.limit(limit)

        result = await self._session.execute(query)
        scalars = result.scalars().all()
        if not scalars:
            return []

        return [scalar.to_entity() for scalar in scalars]


    async def get_batch(self, shorts: set[Short]) -> List[Link]:
        if not shorts:
            return []
        
        short_values = [s.value for s in shorts]
        query = select(LinkORM).where(LinkORM.short.in_(short_values))
        result = await self._session.execute(query)
        scalars = result.scalars().all()
        
        return [link_orm.to_entity() for link_orm in scalars]


    async def increment_redirects_bulk(self, deltas: dict[str, int]) -> None:
        if not deltas:
            return

        values_clause_parts = []
        params = {}

        for short, delta in deltas.items():
            short_escaped = short.replace("'", "''")
            values_clause_parts.append(f"('{short_escaped}'::varchar, {delta}::integer)")

        values_clause = ", ".join(values_clause_parts)

        stmt = text(f"""
            UPDATE link AS l
            SET
                times_used = l.times_used + v.delta,
                last_used = CURRENT_TIMESTAMP AT TIME ZONE 'UTC'
            FROM (VALUES {values_clause}) AS v(short, delta)
            WHERE l.short = v.short
        """)

        await self._session.execute(stmt, params)