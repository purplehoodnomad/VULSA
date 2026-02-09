from enum import Enum
from redis.asyncio import Redis
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Factory

from infrastructure.sqlalchemy.session_manager import DatabaseSessionManager

from infrastructure.postgresql.uow.link import PostgresLinkUnitOfWork
from infrastructure.postgresql.uow.user import PostgresUserUnitOfWork
from infrastructure.postgresql.uow.auth import PostgresAuthUnitOfWork

from infrastructure.inmemory.uow.user import InMemoryUserUnitOfWork

from infrastructure.cache.redis.client import RedisClient

from usecase.common.event_bus import EventBus
from settings import settings


class ContainerUoWTypes(Enum):
    POSTGRES = "postgres"
    INMEMORY = "inmemory"


class Container(DeclarativeContainer):
    uow_type: ContainerUoWTypes = ContainerUoWTypes.POSTGRES
    inmemory_user_storage = Singleton(dict)

    session_manager = Singleton(DatabaseSessionManager)
    event_bus = Singleton(EventBus)

    link_uow_factory = Factory(PostgresLinkUnitOfWork)
    auth_uow_factory = Factory(PostgresAuthUnitOfWork)
    _postgres_user_uow_factory = Factory(PostgresUserUnitOfWork)
    _inmemory_user_uow_factory = Factory(InMemoryUserUnitOfWork)

    redis_client = Singleton(RedisClient)


    @classmethod
    def get_user_uow_factory(cls):
        if cls.uow_type == ContainerUoWTypes.POSTGRES:
            return cls._postgres_user_uow_factory
        if cls.uow_type == ContainerUoWTypes.INMEMORY:
            return cls._inmemory_user_uow_factory
        else:
            raise ValueError(f"Unsupported uow type: {cls.uow_type}")

    @staticmethod
    def get_wired_container() -> "Container":
        container = Container()
        container.wire(
            modules=[
                "infrastructure.sqlalchemy.session",
                "infrastructure.postgresql.di.injection",
            ]
        )
        return container