import asyncio
from datetime import timedelta

from workers.app import app
from container import Container
from settings import settings
from infrastructure.uow.builders import get_link_uow
from usecase.link.delete_expired_links.implementation import DeleteExpiredLinksUseCase


@app.task(name="delete_expired_links", bind=True, acks_late=True)
def delete_expired_links(self):
    async def _run():
        container = Container.get_wired_container()
        
        sessionmanager = container.session_manager()
        sessionmanager.init(settings.database.get_url())

        try:
            async with sessionmanager.session() as session:
                uow = get_link_uow(session)
                usecase = DeleteExpiredLinksUseCase(uow)
                await usecase.execute(timedelta(seconds=10))
        finally:
            # idempotent -> can be "closed" even without init (if task dropped before init)
            await sessionmanager.close()

    loop = asyncio.new_event_loop()
    try:
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(_run())
    
    except Exception as exc: # TODO: add logging
        raise
    finally:
        loop.close()