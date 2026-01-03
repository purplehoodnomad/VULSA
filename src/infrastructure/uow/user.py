from infrastructure.uow.abstract import AbstractUnitOfWork

from domain.user.repository import AbstractUserRepository


class AbstractUserUnitOfWork(AbstractUnitOfWork):
    user_repo: AbstractUserRepository