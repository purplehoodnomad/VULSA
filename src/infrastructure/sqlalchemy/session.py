from typing import AsyncIterator

from fastapi import Depends
from dependency_injector.wiring import inject, Provide
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection

from container import Container

from .session_manager import DatabaseSessionManager


@inject
async def get_async_session(
    session_manager: DatabaseSessionManager = Depends(Provide[Container.session_manager])
) -> AsyncIterator[AsyncSession]:
    async with session_manager.session() as session:
        yield session


@inject
async def get_async_connection(
    session_manager: DatabaseSessionManager = Depends(Provide[Container.session_manager])
) -> AsyncIterator[AsyncConnection]:
    async with session_manager.connect() as connection:
        yield connection