from dataclasses import asdict
from datetime import datetime, timezone

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.sqlalchemy.session import get_async_session
from infrastructure.uow.dependencies import get_link_uow

from infrastructure.broker.abstract.producer import AbstractProducer
from infrastructure.broker.topics import Topic
from usecase.redirect.utils.dto import ClickMetadataDTO

from usecase.redirect.abstract import AbstractLinkRedirectUseCase
from usecase.redirect.implementation import LinkRedirectUseCase


from infrastructure.cache.redis.dependencies import get_link_cache
from domain.link.cache import AbstractLinkCache


async def get_link_redirect_usecase(
    session: AsyncSession = Depends(get_async_session),
    link_cache: AbstractLinkCache = Depends(get_link_cache)
) -> AbstractLinkRedirectUseCase:
    uow = get_link_uow(session)

    return LinkRedirectUseCase(
        uow=uow,
        link_cache=link_cache
    )


async def register_click(
    request: Request,
    producer: AbstractProducer,
) -> None:
    short: str = request.path_params["short"]
    metadata = ClickMetadataDTO(
        short=short,
        timestamp=datetime.now(timezone.utc),
        ip=request.client.host if request.client is not None else None,
        user_agent=request.headers.get("user-agent"),
        referer=request.headers.get("referer"),
        request_url=str(request.url)
    )

    data = asdict(metadata)
    data["timestamp"] = data["timestamp"].isoformat()

    await producer.send(
        topic=Topic.LINK_CLICKED,
        message=data
    )