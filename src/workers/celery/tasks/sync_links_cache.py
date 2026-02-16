import asyncio

from workers.celery.app import app
from workers.dependencies import WorkerContext, get_sync_cache_usecase


@app.task(name="sync_links_cache", bind=True, acks_late=True)
def sync_links_cache(self):
    async def _run():
        async with WorkerContext(with_cache=True) as resources:
            usecase = await get_sync_cache_usecase(resources)
            await usecase.execute()

    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(_run())
    
    except Exception as exc: # TODO: add logging
        self.retry(exc=exc, countdown=10, max_retries=3)
        raise
    finally:
        loop.close()