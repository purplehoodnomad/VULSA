import asyncio
import logging

from workers.celery.app import app
from workers.dependencies import WorkerContext, get_wipe_raw_clicks_usecase


logger = logging.getLogger(__name__)


@app.task(name="wipe_raw_clicks", bind=True, acks_late=True)
def wipe_raw_clicks(self):
    async def _run():
        async with WorkerContext(with_clickhouse=True) as resources:
            usecase = await get_wipe_raw_clicks_usecase(resources)
            await usecase.execute()

    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(_run())
    
    except Exception as exc:
        logger.exception(exc)
        self.retry(exc=exc, countdown=10, max_retries=3)
        raise
    finally:
        loop.close()