from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from databases.postgresql.session import get_async_session
from infrastructure.repositories.postgresql.uow import PostgreSQLLinkUoW

from usecase.link import (
    CreateLinkUsecase, CreateLinkUsecaseImpl,
    GetLinkByIdUseCase, GetLinkByIdUseCaseImpl,
    LinkRedirectUseCase, LinkRedirectUseCaseImpl
)


def get_link_uow(session: AsyncSession = Depends(get_async_session)) -> PostgreSQLLinkUoW:
    return PostgreSQLLinkUoW(session=session)


def get_link_create_usecase(uow: PostgreSQLLinkUoW = Depends(get_link_uow)) -> CreateLinkUsecase:
    return CreateLinkUsecaseImpl(uow)

def get_link_get_by_id_usecase(uow: PostgreSQLLinkUoW = Depends(get_link_uow)) -> GetLinkByIdUseCase:
    return GetLinkByIdUseCaseImpl(uow)

def get_link_redirect_usecase(uow: PostgreSQLLinkUoW = Depends(get_link_uow)) -> LinkRedirectUseCase:
    return LinkRedirectUseCaseImpl(uow)