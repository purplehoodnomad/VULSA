from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.databases.postgresql.session import get_async_session
from infrastructure.di.injection import build_link_uow
from infrastructure.repositories.postgresql.uow import PostgreSQLLinkUoW

from usecase.link import (
    CreateLinkUsecase, CreateLinkUsecaseImpl,
    GetLinkByIdUseCase, GetLinkByIdUseCaseImpl,
    LinkRedirectUseCase, LinkRedirectUseCaseImpl,
    GetLinkListUsecase, GetLinkListUsecaseImpl
)


def get_link_uow(session: AsyncSession = Depends(get_async_session)) -> PostgreSQLLinkUoW:
    return build_link_uow(session)



def get_link_create_usecase(session: AsyncSession = Depends(get_async_session)) -> CreateLinkUsecase:
    uow = get_link_uow(session)
    return CreateLinkUsecaseImpl(uow=uow)


def get_link_get_by_id_usecase(session: AsyncSession = Depends(get_async_session)) -> GetLinkByIdUseCase:
    uow = get_link_uow(session)
    return GetLinkByIdUseCaseImpl(uow=uow)

def get_link_redirect_usecase(session: AsyncSession = Depends(get_async_session)) -> LinkRedirectUseCase:
    uow = get_link_uow(session)
    return LinkRedirectUseCaseImpl(uow=uow)

def get_link_list_usecase(session: AsyncSession = Depends(get_async_session)) -> GetLinkListUsecase:
    uow = get_link_uow(session)
    return GetLinkListUsecaseImpl(uow=uow)