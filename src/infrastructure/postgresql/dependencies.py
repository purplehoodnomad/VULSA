from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from container import Container
from infrastructure.sqlalchemy.session import get_async_session
from infrastructure.clickhouse.dependencies import get_clickhouse_client

from infrastructure.uow.link import AbstractLinkUnitOfWork
from infrastructure.uow.user import AbstractUserUnitOfWork
from infrastructure.uow.auth import AbstractAuthUnitOfWork
from infrastructure.clickhouse.client import ClickHouseClient


def build_link_uow(
    session: AsyncSession = Depends(get_async_session),
    ch_client: ClickHouseClient = Depends(get_clickhouse_client)
) -> AbstractLinkUnitOfWork:
    return Container.link_uow_factory(session=session, ch_client=ch_client)


def build_user_uow(
    session: AsyncSession = Depends(get_async_session),
) -> AbstractUserUnitOfWork:
    user_uow_factory = Container.get_user_uow_factory()
    return user_uow_factory(session)


def build_auth_uow(
    session: AsyncSession = Depends(get_async_session),
) -> AbstractAuthUnitOfWork:
    return Container.auth_uow_factory(session=session)