from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ....domain.link.repository import AbstractLinkRepository
from ....infrastructure.repositories.postgresql.link import PostgresLinkRepository

from ....databases.postgresql.session import get_async_session



def get_link_repo(session: AsyncSession = Depends(get_async_session)) -> AbstractLinkRepository:
    """
    Возвращает конкретную реализацию с универсальными AbstractLinkRepository методами, чтобы не зависеть от варианта реализации репозитория.
    """
    return PostgresLinkRepository(session)