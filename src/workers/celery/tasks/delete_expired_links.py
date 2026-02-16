import asyncio
from datetime import timedelta

from workers.celery.app import app
from workers.dependencies import WorkerContext, get_delete_expired_links_usecase


@app.task(name="delete_expired_links", bind=True, acks_late=True)
def delete_expired_links(self):
    async def _run():
        async with WorkerContext() as resources:
            usecase = await get_delete_expired_links_usecase(resources)
            await usecase.execute(timedelta(days=90))

    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(_run())
    
    except Exception as exc: # TODO: add logging
        raise
    finally:
        loop.close()