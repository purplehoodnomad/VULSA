from infrastructure.uow.abstract import AbstractUnitOfWork

from domain.user.repository import AbstractUserRepository
from domain.token.repository import AbstractTokenRepository


class AbstractAuthUnitOfWork(AbstractUnitOfWork):
    user_repo: AbstractUserRepository
    token_repo: AbstractTokenRepository