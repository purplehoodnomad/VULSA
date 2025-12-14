from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.databases.postgresql.session import get_async_session
from infrastructure.repositories.postgresql.uow import PostgreSQLLinkUoW, PostgreSQLUserUoW
from container import Container


def build_link_uow(session: AsyncSession = Depends(get_async_session)) -> PostgreSQLLinkUoW:
    return Container.link_uow_factory(session=session)


def build_user_uow(session: AsyncSession = Depends(get_async_session)) -> PostgreSQLUserUoW:
    return Container.user_uow_factory(session=session)