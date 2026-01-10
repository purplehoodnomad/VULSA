from abc import ABC, abstractmethod

from domain.repositories.abstract import AbstractRepository
from domain.role.entity import Role
from domain.value_objects.role import RoleName, Permission


class AbstractRoleRepository(AbstractRepository[Role], ABC):
    @abstractmethod
    async def get(self, role_name: RoleName) -> Role:
        raise NotImplementedError