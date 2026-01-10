from abc import ABC, abstractmethod
from uuid import UUID

from usecase.admin.utils.dto import RoleDTO


class AbstractRemovePermissionUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        user_id: UUID,
        role: str,
        permission: str,
    ) -> RoleDTO:
        raise NotImplementedError