from contextlib import asynccontextmanager
from typing import AsyncContextManager, Callable


def make_link_uow_factory(session_manager, container) -> Callable[[], AsyncContextManager]:
    @asynccontextmanager
    async def factory():
        async with session_manager.session() as session:
            uow = container.link_uow_factory(session=session)
            async with uow:
                yield uow
    return factory
