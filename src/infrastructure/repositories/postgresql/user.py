from uuid import UUID

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.databases.postgresql.models import UserORM
from infrastructure.databases.postgresql.exceptions import handle_unique_integrity_error

from domain.user.repository import AbstractUserRepository
from domain.user.entity import User

from domain.value_objects.common import UserId
from domain.value_objects.user import Email
from domain.value_objects.token import Token as TokenVO

from domain.user.exceptions import UserDoesNotExistException, EmailDoesNotExistException


class PostgresUserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session
    
    async def create(self, entity: User) -> User:
        user_orm = UserORM.from_entity(entity)

        self._session.add(user_orm)
        try:
            await self._session.flush()
        except IntegrityError as e:
            handle_unique_integrity_error(e, entity=entity)
        
        return user_orm.to_entity()


    async def get(self, user_id: UserId) -> User:
        """Raises c if no id found"""
        user_orm = await self._session.get(UserORM, user_id.value)

        if user_orm is None:
            raise UserDoesNotExistException(user_id.value)

        return user_orm.to_entity()
    

    async def get_by_email(self, email: Email) -> User:
        """Raises EmailDoesNotExistException if no user with email found"""
        stmt = select(UserORM).where(UserORM.email == email.value)
        result = await self._session.execute(stmt)

        scalar = result.scalar_one_or_none()
        if scalar is None:
            raise EmailDoesNotExistException(email.value)
        
        return scalar.to_entity()

    

    async def delete(self, user_id: UserId) -> None:
        stmt = delete(UserORM).where(UserORM.id == user_id.value)
        await self._session.execute(stmt)


    # async def list(self,
    #     filter: UserFilterDto
    # ) -> list[User]:
    #     expression = []
        
    #     if filter.status is not None:
    #         expression.append(UserORM.status == filter.status)

    #     query = select(UserORM).where(*expression).offset(filter.offset).limit(filter.limit)

    #     result = await self._session.execute(query)
    #     scalars = result.scalars().all()

    #     return [scalar.to_entity() for scalar in scalars]
    

    async def find_user_by_access_token(self, access_token: TokenVO) -> User:
        ...
