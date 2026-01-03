from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from container import Container

from infrastructure.sqlalchemy.session import get_async_session
from infrastructure.postgresql.uow.uow import PostgresLinkUoW, PostgreSQLUserUoW, PostgresAuthUoW


def build_link_uow(session: AsyncSession = Depends(get_async_session)) -> PostgresLinkUoW:
    return Container.link_uow_factory(session=session)


def build_user_uow(session: AsyncSession = Depends(get_async_session)) -> PostgreSQLUserUoW:
    return Container.user_uow_factory(session=session)


def build_auth_uow(session: AsyncSession = Depends(get_async_session)) -> PostgresAuthUoW:
    return Container.auth_uow_factory(session=session)