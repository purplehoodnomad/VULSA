from typing import Union, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.uow.link import AbstractLinkUnitOfWork
from infrastructure.clickhouse.client import ClickHouseClient

from domain.link.repository import AbstractLinkRepository
from domain.user.repository import AbstractUserRepository
from domain.link.repository import AbstractClickStampRepository

from infrastructure.postgresql.repositories.link import PostgresLinkRepository
from infrastructure.postgresql.repositories.user import PostgresUserRepository
from infrastructure.postgresql.repositories.click_stamp import PostgresClickStampRepository
from infrastructure.clickhouse.repositories.click_stamp import ClickHouseClickStampRepository


class PostgresLinkUnitOfWork(AbstractLinkUnitOfWork):
    def __init__(
        self,
        session: AsyncSession,
        *,
        ch_client: Optional[ClickHouseClient] = None
    ):
        self._session: AsyncSession = session
        self._ch_client = ch_client

        self._link_repo: Union[PostgresLinkRepository, None] = None
        self._user_repo: Union[PostgresUserRepository, None] = None
        self._click_repo: Union[PostgresClickStampRepository, ClickHouseClickStampRepository, None] = None

    async def __aenter__(self):
        self._link_repo = PostgresLinkRepository(self._session)
        self._user_repo = PostgresUserRepository(self._session)
        
        if self._ch_client is not None:
            self._click_repo = ClickHouseClickStampRepository(self._ch_client)
        else:
            self._click_repo = PostgresClickStampRepository(self._session)
        
        return self

    async def __aexit__(self, exc_type: Exception | None, exc_val, traceback):
        if exc_type is not None:
            await self.rollback()
        await self.commit()

        await self._session.close()
        self._link_repo = None
        self._user_repo = None
        self._click_repo = None

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
    
    @property
    def link_repo(self) -> AbstractLinkRepository:
        assert self._link_repo is not None
        return self._link_repo

    @property
    def user_repo(self) -> AbstractUserRepository:
        assert self._user_repo is not None
        return self._user_repo

    @property
    def click_repo(self) -> AbstractClickStampRepository:
        assert self._click_repo is not None
        return self._click_repo