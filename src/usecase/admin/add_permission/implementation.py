from uuid import UUID

from infrastructure.uow.user import AbstractUserUnitOfWork

from .abstract import AbstractAddPermissionUseCase

from domain.role.entity import Role
from domain.value_objects.common import UserId
from domain.value_objects.role import Permission, RoleName, RoleDescription

from usecase.admin.utils.dto import RoleDTO


class PostgresAddPermissionUseCase(AbstractAddPermissionUseCase):
    def __init__(self, uow: AbstractUserUnitOfWork):
        self.uow = uow

    async def execute(
        self,
        user_id: UUID,
        role: str,
        permission: str
    ) -> RoleDTO:
        async with self.uow as uow:
            user_entity = await uow.user_repo.get(UserId(user_id))
            user_entity.validate_admin()

            editable_role_entity = await uow.role_repo.get(RoleName(role))
            editable_role_entity.add_permission(Permission(permission))
            
            await uow.role_repo.update(editable_role_entity)
            
            return RoleDTO.from_entity(editable_role_entity)
