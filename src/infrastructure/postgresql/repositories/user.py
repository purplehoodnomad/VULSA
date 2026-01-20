from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.postgresql.models import UserORM
from infrastructure.postgresql.exceptions import handle_unique_integrity_error

from domain.user.repository import AbstractUserRepository
from domain.user.entity import User

from domain.value_objects.common import UserId
from domain.value_objects.user import Email

from domain.user.exceptions import UserNotFound, UserEmailNotFound


class PostgresUserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session
    
    async def create(self, entity: User) -> User:
        user_orm = UserORM.from_entity(entity)

        self._session.add(user_orm)
        try:
            await self._session.flush()
        except IntegrityError as e:
            handle_unique_integrity_error(e)
        
        return user_orm.to_entity()


    async def update(self, entity: User) -> User:
        ...


    async def delete(self, entity: User) -> None:
        await self.delete_by_id(entity.user_id)


    async def delete_by_id(self, user_id: UserId) -> None:
        stmt = delete(UserORM).where(UserORM.id == user_id.value)
        await self._session.execute(stmt)


    async def get(self, user_id: UserId) -> User:
        user_orm = await self._session.get(UserORM, user_id.value)

        if user_orm is None:
            raise UserNotFound()

        return user_orm.to_entity()
    

    async def get_by_email(self, email: Email) -> User:
        stmt = select(UserORM).where(UserORM.email == email.value)
        result = await self._session.execute(stmt)

        scalar = result.scalar_one_or_none()
        if scalar is None:
            raise UserEmailNotFound()
        
        return scalar.to_entity()
