from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Factory

from infrastructure.databases.postgresql.session_manager import DatabaseSessionManager
from infrastructure.repositories.postgresql.uow import PostgresLinkUoW, PostgreSQLUserUoW, PostgresAuthUoW


class Container(DeclarativeContainer):
    session_manager = Singleton(DatabaseSessionManager)

    link_uow_factory = Factory(PostgresLinkUoW)
    user_uow_factory = Factory(PostgreSQLUserUoW)
    auth_uow_factory = Factory(PostgresAuthUoW)