import asyncio

from workers.app import app
from container import Container
from settings import settings
from infrastructure.uow.builders import get_link_uow
from usecase.link.sync_cache.implementation import SyncCacheUseCase
from infrastructure.cache.redis.repositories.link_cache import RedisLinkCache


@app.task(name="sync_links_cache", bind=True, acks_late=True)
def sync_links_cache(self):
    async def _run():
        container = Container.get_wired_container()
        
        sessionmanager = container.session_manager()
        sessionmanager.init(settings.database.get_url())

        redis = container.redis_client()
        redis.init(settings.cache.get_url())

        try:
            cache = RedisLinkCache(redis.client)

            async with sessionmanager.session() as session:
                uow = get_link_uow(session)
                usecase = SyncCacheUseCase(uow, cache)
                await usecase.execute()
        finally:
            # idempotent -> can be "closed" even without init (if task dropped before init)
            await sessionmanager.close()
            await redis.close()

    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(_run())
    
    except Exception as exc: # TODO: add logging
        self.retry(exc=exc, countdown=10, max_retries=3)
        raise
    finally:
        loop.close()