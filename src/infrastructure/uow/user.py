from infrastructure.uow.abstract import AbstractUnitOfWork

from domain.user.repository import AbstractUserRepository
from domain.role.repository import AbstractRoleRepository


class AbstractUserUnitOfWork(AbstractUnitOfWork):
    user_repo: AbstractUserRepository
    role_repo: AbstractRoleRepository