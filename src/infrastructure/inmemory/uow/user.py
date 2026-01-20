from copy import deepcopy

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.uow.user import AbstractUserUnitOfWork
from infrastructure.inmemory.repositories.user import InMemoryUserRepository
from infrastructure.inmemory.repositories.role import InMemoryRoleRepository

from domain.user.entity import User
from domain.value_objects.common import UserId


class InMemoryUserUnitOfWork(AbstractUserUnitOfWork):
    def __init__(self, session: AsyncSession | None = None, storage: dict[UserId, User] = {}):
        self._user_storage = storage
        self._snapshot: dict[UserId, User] | None = None

        self._user_repo: InMemoryUserRepository | None = None
        self._role_repo: InMemoryRoleRepository | None = None

    async def __aenter__(self):
        self._snapshot = deepcopy(self._user_storage)
        self._user_repo = InMemoryUserRepository(self._user_storage)
        self._role_repo = InMemoryRoleRepository()
        return self

    async def __aexit__(self, exc_type: Exception | None, exc_val, traceback):
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()

        self._user_repo = None

    async def commit(self):
        assert self._snapshot is not None
        self._user_storage.clear()
        self._user_storage.update(self._snapshot)

    async def rollback(self):
        pass
    
    @property
    def user_repo(self) -> InMemoryUserRepository:
        assert self._user_repo is not None
        return self._user_repo

    @property
    def role_repo(self) -> InMemoryRoleRepository:
        assert self._role_repo is not None
        return self._role_repo