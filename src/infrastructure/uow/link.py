from infrastructure.uow.abstract import AbstractUnitOfWork

from domain.link.repository import AbstractLinkRepository, AbstractClickStampRepository
from domain.user.repository import AbstractUserRepository


class AbstractLinkUnitOfWork(AbstractUnitOfWork):
    link_repo: AbstractLinkRepository
    user_repo: AbstractUserRepository
    click_repo: AbstractClickStampRepository