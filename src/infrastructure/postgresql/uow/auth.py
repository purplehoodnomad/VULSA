from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.uow.auth import AbstractAuthUnitOfWork

from infrastructure.postgresql.repositories import PostgresUserRepository, PostgresTokenRepository


class PostgresAuthUnitOfWork(AbstractAuthUnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

        self._token_repo: PostgresTokenRepository | None = None
        self._user_repo: PostgresUserRepository | None = None

    async def __aenter__(self):
        self._token_repo = PostgresTokenRepository(self._session)
        self._user_repo = PostgresUserRepository(self._session)
        return self

    async def __aexit__(self, exc_type: Exception | None, exc_val, traceback):
        if exc_type is not None:
            await self.rollback()
        await self.commit()

        await self._session.close()
        self._token_repo = None
        self._user_repo = None

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
    
    @property
    def token_repo(self) -> PostgresTokenRepository:
        assert self._token_repo is not None
        return self._token_repo

    @property
    def user_repo(self) -> PostgresUserRepository:
        assert self._user_repo is not None
        return self._user_repo