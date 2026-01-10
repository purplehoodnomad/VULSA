from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.sqlalchemy.session import get_async_session
from infrastructure.postgresql.di.injection import build_user_uow
from infrastructure.uow.user import AbstractUserUnitOfWork

from usecase.admin.add_permission.abstract import AbstractAddPermissionUseCase
from usecase.admin.remove_permission.abstract import AbstractRemovePermissionUseCase

from usecase.admin.add_permission.implementation import PostgresAddPermissionUseCase
from usecase.admin.remove_permission.implementation import PostgresRemovePermissionUseCase


def get_user_uow(session: AsyncSession = Depends(get_async_session)) -> AbstractUserUnitOfWork:
    return build_user_uow(session)


def get_add_permission_usecase(session: AsyncSession = Depends(get_async_session)) -> AbstractAddPermissionUseCase:
    uow = get_user_uow(session)
    return PostgresAddPermissionUseCase(uow=uow)

def get_remove_permission_usecase(session: AsyncSession = Depends(get_async_session)) -> AbstractRemovePermissionUseCase:
    uow = get_user_uow(session)
    return PostgresRemovePermissionUseCase(uow=uow)
