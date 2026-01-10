from sqlalchemy import select, delete as sql_delete
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.postgresql.models import RoleORM, PermissionORM
from infrastructure.postgresql.exceptions import handle_unique_integrity_error

from domain.role.repository import AbstractRoleRepository
from domain.role.entity import Role
from domain.role.exceptions import RoleNotFound, RolePermissionViolation, PermissionNotFound
from domain.value_objects.role import Permission, RoleName


class PostgresRoleRepository(AbstractRoleRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session
    
    async def create(self, entity: Role) -> None:
        # role = RoleORM.from_entity(entity)

        # self._session.add(role)
        # try:
        #     await self._session.flush()
        # except IntegrityError as e:
        #     handle_unique_integrity_error(e)
        raise NotImplementedError("Use alembic")


    async def update(self, entity: Role) -> None:
        stmt = (
            select(RoleORM)
            .options(selectinload(RoleORM.permissions))
            .where(RoleORM.name == entity.name.value)
        )

        result = await self._session.execute(stmt)
        role_orm = result.scalar_one_or_none()

        if role_orm is None:
            raise RoleNotFound()
        
        current_permissions = {permission.name: permission for permission in role_orm.permissions}

        target_permission_names = {permission.value for permission in entity.permissions}
        
        for perm_name, perm_orm in current_permissions.items():
            if perm_name not in target_permission_names:
                role_orm.permissions.remove(perm_orm)
        
        missing_names = target_permission_names - current_permissions.keys()
        if missing_names:
            stmt = select(PermissionORM).where(
                PermissionORM.name.in_(missing_names)
            )
            result = await self._session.execute(stmt)
            permissions_to_add = result.scalars().all()
            if not permissions_to_add:
                raise PermissionNotFound()
            role_orm.permissions.extend(permissions_to_add)

        try:
            await self._session.flush()
        except IntegrityError as e:
            handle_unique_integrity_error(e)


    async def delete(self, entity: Role) -> None:
        # stmt = sql_delete(RoleORM).where(RoleORM.name == entity.name.value)
        # await self._session.execute(stmt)
        raise NotImplementedError("Use alembic")


    async def get(self, role_name: RoleName) -> Role:
        stmt = (
            select(RoleORM)
            .options(selectinload(RoleORM.permissions))
            .where(RoleORM.name == role_name.value)
        )

        result = await self._session.execute(stmt)
        role = result.scalar_one_or_none()
        if role is None:
            raise RoleNotFound()
        
        return role.to_entity()