from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.databases.postgresql.session import get_async_session
from infrastructure.di.injection import build_user_uow
from infrastructure.repositories.postgresql.uow import PostgreSQLUserUoW

from usecase.user.create_user import AbstractCreateUserUseCase, CreateUserUseCasePostgreSQL
from usecase.user.get_user import AbstractGetUserUseCase, GetUserUseCasePostgreSQL
from usecase.user.delete_user import AbstractDeleteUserUseCase, DeleteUserUseCasePostgreSQL


def get_user_uow(session: AsyncSession = Depends(get_async_session)) -> PostgreSQLUserUoW:
    return build_user_uow(session)



def get_user_create_usecase(session: AsyncSession = Depends(get_async_session)) -> AbstractCreateUserUseCase:
    uow = get_user_uow(session)
    return CreateUserUseCasePostgreSQL(uow=uow)

def get_user_get_usecase(session: AsyncSession = Depends(get_async_session)) -> AbstractGetUserUseCase:
    uow = get_user_uow(session)
    return GetUserUseCasePostgreSQL(uow=uow)

def get_user_delete_usecase(session: AsyncSession = Depends(get_async_session)) -> AbstractDeleteUserUseCase:
    uow = get_user_uow(session)
    return DeleteUserUseCasePostgreSQL(uow=uow)