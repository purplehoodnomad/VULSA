from domain.user.repository import AbstractUserRepository
from domain.user.entity import User

from domain.value_objects.common import UserId
from domain.value_objects.user import Email

from domain.user.exceptions import UserNotFound, UserEmailNotFound, UserAlreadyExists, UserEmailAlreadyExists


class InMemoryUserRepository(AbstractUserRepository):
    def __init__(self, storage: dict[UserId, User]) -> None:
        self._storage = storage
    
    async def create(self, entity: User) -> None:
        user = self._storage.get(entity.user_id, None)
        if user is not None:
            raise UserAlreadyExists()
        
        try:
            await self.get_by_email(entity.email)
            raise UserEmailAlreadyExists()
        except UserEmailNotFound:
            self._storage[entity.user_id] = entity


    async def update(self, entity: User) -> None:
        ...


    async def delete(self, entity: User) -> None:
        del self._storage[entity.user_id]


    async def delete_by_id(self, user_id: UserId) -> None:
        del self._storage[user_id]


    async def get(self, user_id: UserId) -> User:
        try:
            return self._storage[user_id]
        except KeyError:
            raise UserNotFound()
    

    async def get_by_email(self, email: Email) -> User:
        for user in self._storage.values():
            if user.email == email:
                return user
        raise UserEmailNotFound()
