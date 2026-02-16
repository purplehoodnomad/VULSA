from sqlalchemy import select, delete as sql_delete
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.postgresql.models import ClickStampORM

from domain.link.repository import AbstractClickStampRepository
from domain.value_objects.link import ClickStamp


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
    
    
    async def create_batch(self, entities: set[ClickStamp]) -> None:
        if not entities:
            return

        orm_objects = [ClickStampORM.from_entity(e) for e in entities]
        
        self._session.add_all(orm_objects)
        await self._session.flush()