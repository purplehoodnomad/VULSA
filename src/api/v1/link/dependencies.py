from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.sqlalchemy.session import get_async_session
from infrastructure.uow.dependencies import get_link_uow
from infrastructure.cache.redis.dependencies import get_link_cache

from usecase.link.create_link.abstract import AbstractCreateLinkUseCase
from usecase.link.get_links_list.abstract import AbstractGetLinksListUseCase
from usecase.link.delete_short.abstract import AbstractDeleteShortUseCase
from usecase.link.edit_short.abstract import AbstractEditShortLinkUseCase

from usecase.link.create_link.implementation import CreateLinkUseCase
from usecase.link.get_links_list.implementation import GetLinksListUseCase
from usecase.link.delete_short.implementation import DeleteShortUseCase
from usecase.link.edit_short.implementation import EditShortLinkUseCase

from domain.link.cache import AbstractLinkCache


def get_link_create_usecase(session: AsyncSession = Depends(get_async_session)) -> AbstractCreateLinkUseCase:
    uow = get_link_uow(session)
    return CreateLinkUseCase(uow=uow)

def get_get_link_list_usecase(session: AsyncSession = Depends(get_async_session)) -> AbstractGetLinksListUseCase:
    uow = get_link_uow(session)
    return GetLinksListUseCase(uow=uow)

def get_delete_short_usecase(
    session: AsyncSession = Depends(get_async_session),
    link_cache: AbstractLinkCache = Depends(get_link_cache)
) -> AbstractDeleteShortUseCase:
    uow = get_link_uow(session)
    
    return DeleteShortUseCase(uow, link_cache)

def get_edit_short_link_usecase(
    session: AsyncSession = Depends(get_async_session),
    link_cache: AbstractLinkCache = Depends(get_link_cache)
) -> AbstractEditShortLinkUseCase:
    uow = get_link_uow(session)
    
    return EditShortLinkUseCase(uow, link_cache)