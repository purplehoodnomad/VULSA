from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Factory

from infrastructure.sqlalchemy.session_manager import DatabaseSessionManager

from infrastructure.postgresql.uow.link import PostgresLinkUnitOfWork
from infrastructure.postgresql.uow.user import PostgresUserUnitOfWork
from infrastructure.postgresql.uow.auth import PostgresAuthUnitOfWork


class Container(DeclarativeContainer):
    session_manager = Singleton(DatabaseSessionManager)

    link_uow_factory = Factory(PostgresLinkUnitOfWork)
    user_uow_factory = Factory(PostgresUserUnitOfWork)
    auth_uow_factory = Factory(PostgresAuthUnitOfWork)