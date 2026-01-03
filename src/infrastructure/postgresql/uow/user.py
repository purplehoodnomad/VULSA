from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.uow.user import AbstractUserUnitOfWork

from infrastructure.postgresql.repositories import PostgresUserRepository


class PostgresUserUnitOfWork(AbstractUserUnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

        self.user_repo: PostgresUserRepository | None = None

    async def __aenter__(self):
        self.user_repo = PostgresUserRepository(self._session)
        return self

    async def __aexit__(self, exc_type: Exception | None, exc_val, traceback):
        if exc_type is not None:
            await self.rollback()
        await self.commit()

        await self._session.close()
        self.user_repo = None

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()