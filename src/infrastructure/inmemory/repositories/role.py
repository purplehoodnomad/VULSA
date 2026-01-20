from domain.role.repository import AbstractRoleRepository
from domain.role.entity import Role
from domain.role.exceptions import RoleNotFound
from domain.value_objects.role import RoleName, RoleDescription


storage: dict[RoleName, Role] = {
    RoleName("user"): Role(name=RoleName("user"), description=RoleDescription("sex"), permissions=set()),
    RoleName("admin"): Role(name=RoleName("admin"), description=RoleDescription("dozens of sex"), permissions=set())
}

class InMemoryRoleRepository(AbstractRoleRepository):
    def __init__(self, storage: dict[RoleName, Role] = storage) -> None:
        self._role_storage = storage
    
    async def create(self, entity: Role) -> None:
        raise NotImplementedError("Not used for testing")

    async def update(self, entity: Role) -> None:
        raise NotImplementedError("Not used for testing")

    async def delete(self, entity: Role) -> None:
        raise NotImplementedError("Not used for testing")


    async def get(self, role_name: RoleName) -> Role:
        role = self._role_storage.get(role_name)
        if role is None:
            raise RoleNotFound()

        return role