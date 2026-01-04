from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.uow.link import AbstractLinkUnitOfWork

from infrastructure.postgresql.repositories.link import PostgresLinkRepository
from infrastructure.postgresql.repositories.user import PostgresUserRepository


class PostgresLinkUnitOfWork(AbstractLinkUnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

        self._link_repo: PostgresLinkRepository | None = None
        self._user_repo: PostgresUserRepository | None = None

    async def __aenter__(self):
        self._link_repo = PostgresLinkRepository(self._session)
        self._user_repo = PostgresUserRepository(self._session)
        return self

    async def __aexit__(self, exc_type: Exception | None, exc_val, traceback):
        if exc_type is not None:
            await self.rollback()
        await self.commit()

        await self._session.close()
        self._link_repo = None
        self._user_repo = None

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
    
    @property
    def link_repo(self) -> PostgresLinkRepository:
        assert self._link_repo is not None
        return self._link_repo

    @property
    def user_repo(self) -> PostgresUserRepository:
        assert self._user_repo is not None
        return self._user_repo