from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.sqlalchemy.session import get_async_session
from infrastructure.uow.builders import get_auth_uow

from usecase.auth.refresh.abstract import AbstractRefreshAccessTokenUseCase
from usecase.auth.login.abstract import AbstractLoginUseCase

from usecase.auth.refresh.implementation import PostgresRefreshAccessTokenUseCase
from usecase.auth.login.implementation import PostgresLoginUseCase


def get_refresh_access_token_usecase(session: AsyncSession = Depends(get_async_session)) -> AbstractRefreshAccessTokenUseCase:
    uow = get_auth_uow(session)
    return PostgresRefreshAccessTokenUseCase(uow=uow)

def get_login_usecase(session: AsyncSession = Depends(get_async_session)) -> AbstractLoginUseCase:
    uow = get_auth_uow(session)
    return PostgresLoginUseCase(uow=uow)