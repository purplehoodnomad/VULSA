from abc import ABC, abstractmethod

from domain.repositories.abstract import AbstractRepository

from domain.value_objects.common import UserId
from domain.value_objects.user import Email

from .entity import User


class AbstractUserRepository(AbstractRepository[User], ABC):
    @abstractmethod
    async def delete_by_id(self, user_id: UserId) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def get(self, user_id: UserId) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: Email) -> User:
        raise NotImplementedError