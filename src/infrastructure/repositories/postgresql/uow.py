from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.repositories.postgresql import PostgresLinkRepository, PostgresUserRepository


class PostgreSQLLinkUoW:
    """TODO нет абстракции UoW и это хуево"""
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

        self.repository: PostgresLinkRepository | None = None

    async def __aenter__(self):
        self.repository = PostgresLinkRepository(self._session)
        return self

    async def __aexit__(self, exc_type: Exception | None, exc_val, traceback):
        if exc_type is not None:
            await self.rollback()
        await self.commit()

        await self._session.close()
        self.repository = None

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()


class PostgreSQLUserUoW:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

        self.repository: PostgresUserRepository | None = None

    async def __aenter__(self):
        self.repository = PostgresUserRepository(self._session)
        return self

    async def __aexit__(self, exc_type: Exception | None, exc_val, traceback):
        if exc_type is not None:
            await self.rollback()
        await self.commit()

        await self._session.close()
        self.repository = None

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()