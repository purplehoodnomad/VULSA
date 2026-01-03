from abc import ABC, abstractmethod
from uuid import UUID

from usecase.user.utils.dto import UserDTO


class AbstractGetUserByIdUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        user_id: UUID
    ) -> UserDTO:
        raise NotImplementedError