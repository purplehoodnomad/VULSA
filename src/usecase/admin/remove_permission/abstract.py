from abc import ABC, abstractmethod

from usecase.admin.utils.dto import RoleDTO, EditPermissionDTO


class AbstractRemovePermissionUseCase(ABC):
    @abstractmethod
    async def execute(self, dto: EditPermissionDTO) -> RoleDTO:
        raise NotImplementedError