from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.databases.postgresql.models import UserORM

from domain.user.repository import AbstractUserRepository
from domain.user.entity import User
from domain.common.value_objects import UserId
from domain.user.exceptions import UserDoesNotExist
from domain.user.repository import UserFilterDto


class PostgresUserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session
    
    async def create(self, entity: User) -> User:
        user_orm = UserORM.from_entity(entity)

        self._session.add(user_orm)
        await self._session.flush()
        
        return user_orm.to_entity()


    async def get(self, user_id: UserId) -> User:
        user_orm = await self._session.get(UserORM, user_id.value)

        if user_orm is None:
            raise UserDoesNotExist()

        return user_orm.to_entity()


    async def list(self,
        filter: UserFilterDto
    ) -> list[User]:
        expression = []
        
        if filter.status is not None:
            expression.append(UserORM.status == filter.status)

        query = select(UserORM).where(*expression).offset(filter.offset).limit(filter.limit)

        result = await self._session.execute(query)
        scalars = result.scalars().all()

        return [scalar.to_entity() for scalar in scalars]
