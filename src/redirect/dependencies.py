from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.sqlalchemy.session import get_async_session
from infrastructure.postgresql.di.injection import build_link_uow
from infrastructure.postgresql.uow.link import AbstractLinkUnitOfWork

from usecase.redirect.abstract import AbstractLinkRedirectUseCase
from usecase.redirect.implementation import PostgresLinkRedirectUseCase


def get_link_uow(session: AsyncSession = Depends(get_async_session)) -> AbstractLinkUnitOfWork:
    return build_link_uow(session)


def get_link_redirect_usecase(session: AsyncSession = Depends(get_async_session)) -> AbstractLinkRedirectUseCase:
    uow = get_link_uow(session)
    return PostgresLinkRedirectUseCase(uow=uow)
