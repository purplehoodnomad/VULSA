from abc import ABC

from domain.repositories.abstract import AbstractRepository
from domain.value_objects.common import UserId

from .entity import User


class AbstractUserRepository(AbstractRepository[User, UserId], ABC):
    pass