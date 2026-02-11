from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.sqlalchemy.session import get_async_session
from infrastructure.uow.builders import get_link_uow
from infrastructure.postgresql.di.injection import get_event_bus

from usecase.redirect.abstract import AbstractLinkRedirectUseCase
from usecase.redirect.implementation import LinkRedirectUseCase
from usecase.redirect.utils.dto import ClickMetadataDTO

from api.v1.dependencies import subscribe_link_events
from usecase.common.event_bus import EventBus

from infrastructure.cache.redis.di.injection import get_link_cache
from domain.link.cache import AbstractLinkCache


async def get_link_redirect_usecase(
    session: AsyncSession = Depends(get_async_session),
    event_bus: EventBus = Depends(get_event_bus),
    link_cache: AbstractLinkCache = Depends(get_link_cache)
) -> AbstractLinkRedirectUseCase:
    uow = get_link_uow(session)

    event_bus = subscribe_link_events(
        event_bus=event_bus,
        uow=uow,
    )

    return LinkRedirectUseCase(
        uow=uow,
        event_bus=event_bus,
        link_cache=link_cache
    )


async def get_click_metadata(request: Request) -> ClickMetadataDTO:
    return ClickMetadataDTO(
        ip=request.client.host if request.client is not None else None,
        user_agent=request.headers.get("user-agent"),
        referer=request.headers.get("referer"),
        request_url=str(request.url)
    )