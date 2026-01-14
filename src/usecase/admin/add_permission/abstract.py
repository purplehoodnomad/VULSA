from abc import ABC, abstractmethod

from usecase.admin.utils.dto import RoleDTO, EditPermissionDTO


class AbstractAddPermissionUseCase(ABC):
    @abstractmethod
    async def execute(self, dto: EditPermissionDTO) -> RoleDTO:
        raise NotImplementedError