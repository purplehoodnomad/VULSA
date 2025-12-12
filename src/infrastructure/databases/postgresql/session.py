from typing import AsyncIterator

from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.databases.postgresql.session_manager import DatabaseSessionManager
from container import Container


@inject
async def get_async_session(
    session_manager: DatabaseSessionManager = Depends(Provide[Container.session_manager])
) -> AsyncIterator[AsyncSession]:
    async with session_manager.session() as session:
        yield session