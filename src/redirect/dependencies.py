from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.sqlalchemy.session import get_async_session
from infrastructure.postgresql.di.injection import build_link_uow
from infrastructure.postgresql.uow.link import AbstractLinkUnitOfWork

from usecase.redirect.abstract import AbstractLinkRedirectUseCase
from usecase.redirect.implementation import PostgresLinkRedirectUseCase
from usecase.redirect.utils.dto import ClickMetadataDTO

from api.v1.dependencies import get_event_bus
from usecase.common.event_bus import EventBus


async def get_link_uow(session: AsyncSession = Depends(get_async_session)) -> AbstractLinkUnitOfWork:
    return build_link_uow(session)


async def get_link_redirect_usecase(
    session: AsyncSession = Depends(get_async_session),
    event_bus: EventBus = Depends(get_event_bus)
) -> AbstractLinkRedirectUseCase:
    uow = await get_link_uow(session)
    return PostgresLinkRedirectUseCase(uow=uow, event_bus=event_bus)


async def get_click_metadata(request: Request) -> ClickMetadataDTO:
    return ClickMetadataDTO(
        ip=request.client.host if request.client is not None else None,
        user_agent=request.headers.get("user-agent"),
        referer=request.headers.get("referer"),
        request_url=str(request.url)
    )