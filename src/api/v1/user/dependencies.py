from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.sqlalchemy.session import get_async_session
from infrastructure.uow.dependencies import get_user_uow
from infrastructure.uow.dependencies import get_auth_uow

from usecase.user.create_user.abstract import AbstractCreateUserUseCase
from usecase.user.get_user_by_id.abstract import AbstractGetUserByIdUseCase
from usecase.user.delete_user.abstract import AbstractDeleteUserUseCase
from usecase.user.get_current_user.abstract import AbstractGetCurrentUserUseCase

from usecase.user.create_user.implementation import CreateUserUseCase
from usecase.user.get_user_by_id.implementation import GetUserByIdUseCase
from usecase.user.delete_user.implementation import DeleteUserUseCase
from usecase.user.get_current_user.implementation import GetCurrentUserUseCase


def get_create_user_usecase(session: AsyncSession = Depends(get_async_session)) -> AbstractCreateUserUseCase:
    uow = get_user_uow(session)
    return CreateUserUseCase(uow=uow)

def get_get_user_by_id_usecase(session: AsyncSession = Depends(get_async_session)) -> AbstractGetUserByIdUseCase:
    uow = get_user_uow(session)
    return GetUserByIdUseCase(uow=uow)

def get_delete_user_usecase(session: AsyncSession = Depends(get_async_session)) -> AbstractDeleteUserUseCase:
    uow = get_user_uow(session)
    return DeleteUserUseCase(uow=uow)

def get_get_current_user_usecase(session: AsyncSession = Depends(get_async_session)) -> AbstractGetCurrentUserUseCase:
    uow = get_auth_uow(session)
    return GetCurrentUserUseCase(uow=uow)