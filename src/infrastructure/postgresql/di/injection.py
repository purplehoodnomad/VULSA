from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from dependency_injector.wiring import inject, Provide

from container import Container
from infrastructure.sqlalchemy.session import get_async_session

from infrastructure.uow.link import AbstractLinkUnitOfWork
from infrastructure.uow.user import AbstractUserUnitOfWork
from infrastructure.uow.auth import AbstractAuthUnitOfWork

from usecase.common.event_bus import EventBus


def build_link_uow(
    session: AsyncSession = Depends(get_async_session),
) -> AbstractLinkUnitOfWork:
    return Container.link_uow_factory(session=session)


def build_user_uow(
    session: AsyncSession = Depends(get_async_session),
) -> AbstractUserUnitOfWork:
    user_uow_factory = Container.get_user_uow_factory()
    return user_uow_factory(session)


def build_auth_uow(
    session: AsyncSession = Depends(get_async_session),
) -> AbstractAuthUnitOfWork:
    return Container.auth_uow_factory(session=session)


@inject
def get_event_bus(
    event_bus: EventBus = Depends(Provide[Container.event_bus])
) -> EventBus:
    return event_bus