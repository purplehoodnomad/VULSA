from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.sqlalchemy.session import get_async_session
from infrastructure.postgresql.di.injection import build_link_uow, build_user_uow, build_auth_uow
from infrastructure.uow.link import AbstractLinkUnitOfWork
from infrastructure.uow.user import AbstractUserUnitOfWork
from infrastructure.uow.auth import AbstractAuthUnitOfWork


def get_link_uow(session: AsyncSession = Depends(get_async_session)) -> AbstractLinkUnitOfWork:
    return build_link_uow(session)

def get_user_uow(session: AsyncSession = Depends(get_async_session)) -> AbstractUserUnitOfWork:
    return build_user_uow(session)

def get_auth_uow(session: AsyncSession = Depends(get_async_session)) -> AbstractAuthUnitOfWork:
    return build_auth_uow(session)