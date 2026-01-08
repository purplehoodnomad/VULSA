

from sqlalchemy import select, delete as sql_delete
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.postgresql.models import ClickStampORM

from domain.click_stamp.repository import AbstractClickStampRepository
from domain.click_stamp.entity import ClickStamp


class PostgresClickStampRepository(AbstractClickStampRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session
    
    async def create(self, entity: ClickStamp) -> ClickStamp:
        stamp_orm = ClickStampORM.from_entity(entity)

        self._session.add(stamp_orm)
        await self._session.flush()
        
        return stamp_orm.to_entity()
    
    async def update(self, entity: ClickStamp) -> None:
        raise NotImplementedError
    
    async def delete(self, entity: ClickStamp) -> None:
        raise NotImplementedError