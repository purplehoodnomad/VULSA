from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.databases.postgresql.session import get_async_session
from infrastructure.di.injection import build_link_uow
from infrastructure.repositories.postgresql.uow import PostgresLinkUoW

from usecase.link.redirect import AbstractLinkRedirectUseCase, PostgresLinkRedirectUseCase


def get_link_uow(session: AsyncSession = Depends(get_async_session)) -> PostgresLinkUoW:
    return build_link_uow(session)


def get_link_redirect_usecase(session: AsyncSession = Depends(get_async_session)) -> AbstractLinkRedirectUseCase:
    uow = get_link_uow(session)
    return PostgresLinkRedirectUseCase(uow=uow)
