from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.databases.postgresql.session import get_async_session
from infrastructure.di.injection import build_auth_uow
from infrastructure.repositories.postgresql.uow import PostgresAuthUoW

from usecase.auth.refresh import AbstractRefreshAccessTokenUseCase, PostgresRefreshAccessTokenUseCase
from usecase.auth.login import AbstractLoginUseCase, PostgresLoginUseCase


def get_auth_uow(session: AsyncSession = Depends(get_async_session)) -> PostgresAuthUoW:
    return build_auth_uow(session)

def get_refresh_access_token_usecase(session: AsyncSession = Depends(get_async_session)) -> AbstractRefreshAccessTokenUseCase:
    uow = get_auth_uow(session)
    return PostgresRefreshAccessTokenUseCase(uow=uow)

def get_login_usecase(session: AsyncSession = Depends(get_async_session)) -> AbstractLoginUseCase:
    uow = get_auth_uow(session)
    return PostgresLoginUseCase(uow=uow)