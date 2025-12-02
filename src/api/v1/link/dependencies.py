from ....domain.link.repository import AbstractLinkRepository
from ....infrastructure.repositories.inmemory.link import InMemoryLinkRepository


_link_repo = InMemoryLinkRepository()


def get_link_repo() -> AbstractLinkRepository:
    """
    Возвращает конкретную реализацию с универсальными AbstractLinkRepository методами, чтобы не зависеть от варианта реализации репозитория.
    """
    return _link_repo