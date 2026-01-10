from domain.value_objects.role import RoleName, RoleDescription, Permission
from domain.role.exceptions import RolePermissionViolation


class Role:
    """Role entity"""

    def __init__(
        self,
        *,
        name: RoleName,
        description: RoleDescription,
        permissions: set[Permission]
    ):
        self._name = name
        self._description = description
        self._permissions = permissions


    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, Role):
            return self.name == obj.name
        return False
    
    @property
    def name(self) -> RoleName:
        return self._name
    
    @property
    def description(self) -> RoleDescription:
        return self._description
    
    @property
    def permissions(self) -> set[Permission]:
        return self._permissions
    

    @staticmethod
    def create(*,
        name: RoleName,
        description: RoleDescription
    ) -> "Role":
        """Creates Role entity"""

        return Role(
            name=name,
            description=description,
            permissions=set()
        )
    
    def add_permission(self, permission: Permission) -> None:
        self._permissions.add(permission)

    def remove_permission(self, permission: Permission) -> None:
        self._permissions.discard(permission)

    def validate_permission(self, permission: Permission) -> None:
        if not permission in self._permissions:
            raise RolePermissionViolation()