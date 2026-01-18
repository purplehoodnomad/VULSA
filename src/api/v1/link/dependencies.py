from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.sqlalchemy.session import get_async_session
from infrastructure.uow.builders import get_link_uow

from usecase.link.create_link.abstract import AbstractCreateLinkUseCase
from usecase.link.get_links_list.abstract import AbstractGetLinksListUseCase
from usecase.link.delete_short.abstract import AbstractDeleteShortUseCase
from usecase.link.edit_short.abstract import AbstractEditShortLinkUseCase

from usecase.link.create_link.implementation import PostgresCreateLinkUseCase
from usecase.link.get_links_list.implementation import PostgresGetLinksListUseCase
from usecase.link.delete_short.implementation import PostgresDeleteShortUseCase
from usecase.link.edit_short.implementation import PostgresEditShortLinkUseCase


def get_link_create_usecase(session: AsyncSession = Depends(get_async_session)) -> AbstractCreateLinkUseCase:
    uow = get_link_uow(session)
    return PostgresCreateLinkUseCase(uow=uow)

def get_get_link_list_usecase(session: AsyncSession = Depends(get_async_session)) -> AbstractGetLinksListUseCase:
    uow = get_link_uow(session)
    return PostgresGetLinksListUseCase(uow=uow)

def get_delete_short_usecase(session: AsyncSession = Depends(get_async_session)) -> AbstractDeleteShortUseCase:
    uow = get_link_uow(session)
    return PostgresDeleteShortUseCase(uow=uow)

def get_edit_short_link_usecase(session: AsyncSession = Depends(get_async_session)) -> AbstractEditShortLinkUseCase:
    uow = get_link_uow(session)
    return PostgresEditShortLinkUseCase(uow=uow)

