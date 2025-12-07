from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from databases.postgresql.session import get_async_session
from infrastructure.repositories.postgresql.uow import PostgreSQLLinkUoW

from usecase.link import (
    CreateLinkUsecase, CreateLinkUsecaseImpl
)


def get_link_uow(session: AsyncSession = Depends(get_async_session)) -> PostgreSQLLinkUoW:
    return PostgreSQLLinkUoW(session=session)


def get_link_create_usecase(uow: PostgreSQLLinkUoW = Depends(get_link_uow)) -> CreateLinkUsecase:
    return CreateLinkUsecaseImpl(uow)