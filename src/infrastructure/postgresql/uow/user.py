from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.uow.user import AbstractUserUnitOfWork

from infrastructure.postgresql.repositories import PostgresUserRepository, PostgresRoleRepository


class PostgresUserUnitOfWork(AbstractUserUnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

        self._user_repo: PostgresUserRepository | None = None
        self._role_repo: PostgresRoleRepository | None = None

    async def __aenter__(self):
        self._user_repo = PostgresUserRepository(self._session)
        self._role_repo = PostgresRoleRepository(self._session)
        return self

    async def __aexit__(self, exc_type: Exception | None, exc_val, traceback):
        if exc_type is not None:
            await self.rollback()
        await self.commit()

        await self._session.close()
        self._user_repo = None
        self._role_repo = None

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
    
    @property
    def user_repo(self) -> PostgresUserRepository:
        assert self._user_repo is not None
        return self._user_repo

    @property
    def role_repo(self) -> PostgresRoleRepository:
        assert self._role_repo is not None
        return self._role_repo