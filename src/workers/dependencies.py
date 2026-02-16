from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from aiokafka import AIOKafkaConsumer

from workers.celery.container import container
from settings import settings

from infrastructure.uow.builders import get_link_uow
from domain.link.cache import AbstractLinkCache
from infrastructure.cache.redis.repositories.link_cache import RedisLinkCache

from usecase.link.delete_expired_links.abstract import AbstractDeleteExpiredLinksUseCase
from usecase.link.sync_cache.abstract import AbstractSyncCacheUseCase
from usecase.link.resolve_clicks.abstract import AbstractResolveClicksUseCase

from usecase.link.delete_expired_links.implementation import DeleteExpiredLinksUseCase
from usecase.link.sync_cache.implementation import SyncCacheUseCase
from usecase.link.resolve_clicks.implementation import ResolveClicksUseCase


@dataclass(slots=True, frozen=True)
class WorkerResources:
    session: AsyncSession
    cache: AbstractLinkCache | None = None
    consumer: AIOKafkaConsumer | None = None


class WorkerContext:
    def __init__(
        self,
        *,
        with_cache: bool = False
    ):
        self._container = container
        self._cache = None
        self._kafka = None

        self._session_manager = self._container.session_manager()
        self._session_manager.init(settings.database.get_url())

        if with_cache and self._cache is None:
            self._redis = self._container.redis_client()
            self._redis.init(settings.cache.get_url())
            self._cache = RedisLinkCache(self._redis.client)
        else:
            self._redis = None
            self._cache = None


    async def __aenter__(self) -> WorkerResources:
        self._session_ctx = self._session_manager.session()
        session = await self._session_ctx.__aenter__()

        return WorkerResources(
            session=session,
            cache=self._cache
        )

    async def __aexit__(self, exc_type, exc, tb):
        await self._session_ctx.__aexit__(exc_type, exc, tb)
        await self._session_manager.close()
        if self._redis is not None:
            await self._redis.close()



async def get_sync_cache_usecase(resources: WorkerResources) -> AbstractSyncCacheUseCase:
    uow = get_link_uow(resources.session)

    return SyncCacheUseCase(
        uow=uow,
        cache=resources.cache # type: ignore
    )


async def get_delete_expired_links_usecase(resources: WorkerResources) -> AbstractDeleteExpiredLinksUseCase:
    uow = get_link_uow(resources.session)

    return DeleteExpiredLinksUseCase(uow=uow)


async def get_resolve_clicks_usecase(resources: WorkerResources) -> AbstractResolveClicksUseCase:
    uow = get_link_uow(resources.session)

    return ResolveClicksUseCase(
        uow=uow,
        consumer=resources.consumer # type: ignore
    )