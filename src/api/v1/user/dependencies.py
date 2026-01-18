from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.sqlalchemy.session import get_async_session
from infrastructure.uow.builders import get_user_uow
from infrastructure.uow.builders import get_auth_uow

from usecase.user.create_user.abstract import AbstractCreateUserUseCase
from usecase.user.get_user_by_id.abstract import AbstractGetUserByIdUseCase
from usecase.user.delete_user.abstract import AbstractDeleteUserUseCase
from usecase.user.get_current_user.abstract import AbstractGetCurrentUserUseCase

from usecase.user.create_user.implementation import PostgresCreateUserUseCase
from usecase.user.get_user_by_id.implementation import PostgresGetUserByIdUseCase
from usecase.user.delete_user.implementation import PostgresDeleteUserUseCase
from usecase.user.get_current_user.implementation import PostgresGetCurrentUserUseCase


def get_create_user_usecase(session: AsyncSession = Depends(get_async_session)) -> AbstractCreateUserUseCase:
    uow = get_user_uow(session)
    return PostgresCreateUserUseCase(uow=uow)

def get_get_user_by_id_usecase(session: AsyncSession = Depends(get_async_session)) -> AbstractGetUserByIdUseCase:
    uow = get_user_uow(session)
    return PostgresGetUserByIdUseCase(uow=uow)

def get_delete_user_usecase(session: AsyncSession = Depends(get_async_session)) -> AbstractDeleteUserUseCase:
    uow = get_user_uow(session)
    return PostgresDeleteUserUseCase(uow=uow)

def get_get_current_user_usecase(session: AsyncSession = Depends(get_async_session)) -> AbstractGetCurrentUserUseCase:
    uow = get_auth_uow(session)
    return PostgresGetCurrentUserUseCase(uow=uow)