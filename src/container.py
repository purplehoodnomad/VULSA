from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Factory

from infrastructure.databases.postgresql.session_manager import DatabaseSessionManager
from infrastructure.repositories.postgresql.uow import PostgreSQLLinkUoW, PostgreSQLUserUoW


class Container(DeclarativeContainer):
    session_manager = Singleton(DatabaseSessionManager)

    link_uow_factory = Factory(PostgreSQLLinkUoW)
    user_uow_factory = Factory(PostgreSQLUserUoW)